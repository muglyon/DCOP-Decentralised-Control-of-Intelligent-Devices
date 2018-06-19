namespace ComputerVisionModule
{
    using Newtonsoft.Json;                
    using System;
    using System.IO;
    using System.Runtime.InteropServices;
    using System.Runtime.Loader;
    using System.Security.Cryptography.X509Certificates;
    using System.Text;
    using System.Threading;
    using System.Threading.Tasks;
    using Microsoft.Azure.Devices.Client;
    using Microsoft.Azure.Devices.Client.Transport.Mqtt;
    using System.Net.Http;
    using Newtonsoft.Json.Linq;
    using OpenCvSharp;

    class Program
    {
        // public static String FILENAME = @"temp.bmp";
        public static String FILENAME = @"temp.bmp";
        public static String EMOTION_API = "http://127.0.0.1/image";

        // static int counter;

        static void Main(string[] args)
        {
            // The Edge runtime gives us the connection string we need -- it is injected as an environment variable
            string connectionString = "HostName=slh-iot-hub.azure-devices.net;GatewayHostName=inv010825.viseo.net;DeviceId=camera;ModuleId=computervisionmodule;SharedAccessKey=6zR3jQslASSaWwSXnxZAZl1uw3RA2DJ8RVHn1GlEXSk=";
            //string connectionString = Environment.GetEnvironmentVariable("EdgeHubConnectionString");

            // Cert verification is not yet fully functional when using Windows OS for the container
            bool bypassCertVerification = RuntimeInformation.IsOSPlatform(OSPlatform.Windows);
            if (!bypassCertVerification) InstallCert();
            Init(connectionString, bypassCertVerification).Wait();

            // Wait until the app unloads or is cancelled
            var cts = new CancellationTokenSource();
            AssemblyLoadContext.Default.Unloading += (ctx) => cts.Cancel();
            Console.CancelKeyPress += (sender, cpe) => cts.Cancel();
            WhenCancelled(cts.Token).Wait();
        }

        /// <summary>
        /// Handles cleanup operations when app is cancelled or unloads
        /// </summary>
        public static Task WhenCancelled(CancellationToken cancellationToken)
        {
            var tcs = new TaskCompletionSource<bool>();
            cancellationToken.Register(s => ((TaskCompletionSource<bool>)s).SetResult(true), tcs);
            return tcs.Task;
        }

        /// <summary>
        /// Add certificate in local cert store for use by client for secure connection to IoT Edge runtime
        /// </summary>
        static void InstallCert()
        {
            string certPath = Environment.GetEnvironmentVariable("EdgeModuleCACertificateFile");
            if (string.IsNullOrWhiteSpace(certPath))
            {
                // We cannot proceed further without a proper cert file
                Console.WriteLine($"Missing path to certificate collection file: {certPath}");
                throw new InvalidOperationException("Missing path to certificate file.");
            }
            else if (!File.Exists(certPath))
            {
                // We cannot proceed further without a proper cert file
                Console.WriteLine($"Missing path to certificate collection file: {certPath}");
                throw new InvalidOperationException("Missing certificate file.");
            }
            X509Store store = new X509Store(StoreName.Root, StoreLocation.CurrentUser);
            store.Open(OpenFlags.ReadWrite);
            store.Add(new X509Certificate2(X509Certificate2.CreateFromCertFile(certPath)));
            Console.WriteLine("Added Cert: " + certPath);
            store.Close();
        }


        /// <summary>
        /// Initializes the DeviceClient and sets up the callback to receive
        /// messages containing temperature information
        /// </summary>
        static async Task Init(string connectionString, bool bypassCertVerification = false)
        {
            Console.WriteLine("Connection String {0}", connectionString);

            MqttTransportSettings mqttSetting = new MqttTransportSettings(TransportType.Mqtt_Tcp_Only);
            // During dev you might want to bypass the cert verification. It is highly recommended to verify certs systematically in production
            if (bypassCertVerification)
            {
                mqttSetting.RemoteCertificateValidationCallback = (sender, certificate, chain, sslPolicyErrors) => true;
            }
            ITransportSettings[] settings = { mqttSetting };

            // Open a connection to the Edge runtime
            DeviceClient ioTHubModuleClient = DeviceClient.CreateFromConnectionString(connectionString, settings);
            await ioTHubModuleClient.OpenAsync();
            Console.WriteLine("IoT Hub module client initialized.");

            // Register callback to be called when a message is received by the module
            await SendDeviceToCloudMessagesAsync(ioTHubModuleClient);
        }

        static async Task<MessageResponse> SendDeviceToCloudMessagesAsync(DeviceClient userContext)
        {

            Random rand = new Random();

            DeviceClient deviceClient = (DeviceClient) userContext;

            while (true)
            {
                double currentBatteryVoltage = rand.Next(20, 40);
                double currentResponseTime = rand.Next(2, 6); 
                double currentAmbientTemperature = rand.Next(10, 30);
                double currentHumidity = rand.Next(5, 80);

                // VideoCapture capture = new VideoCapture();
                // capture.Open(0);

                // using (Mat image = new Mat()) 
                // {
                //     capture.Read(image);
                //     image.SaveImage(FILENAME);
                // }

                MessageBody messageBody = new MessageBody();
                // messageBody.happyProbability = 0.0;
                // messageBody.sadProbability = 0.0;

                // submitToModelAsync(messageBody).Wait();

                Machine drone = new Machine();
                drone.batteryVoltage = currentBatteryVoltage;
                drone.responseTime = currentResponseTime;

                Ambient ambient = new Ambient();
                ambient.temperature = currentAmbientTemperature;
                ambient.humidity = currentHumidity;

                // messageBody.ambient = ambient;
                // messageBody.drone = drone;

                var messageString = JsonConvert.SerializeObject(messageBody);
                var message = new Message(Encoding.ASCII.GetBytes(messageString));

                await deviceClient.SendEventAsync("output1", message);

                await Task.Delay(1000);
            }
        }

        static async Task submitToModelAsync(MessageBody messageBody)
        {
            var client = new HttpClient();
            byte[] byteFile = new byte[1024];

            using (System.IO.FileStream fs = File.Open(FILENAME, FileMode.Open))
            {
                byteFile = new byte[(int)fs.Length];
                fs.Read(byteFile, 0, (int)fs.Length);
            }

            // Get the response.
            HttpResponseMessage response = await client.PostAsync(
                EMOTION_API,
                new ByteArrayContent(byteFile));
            
            using (var reader = new StreamReader(await response.Content.ReadAsStreamAsync()))
            {
                var result = await reader.ReadToEndAsync();
                JObject jsonResult = JObject.Parse(result);

                foreach (var prediction in jsonResult["predictions"])
                {
                    if(prediction["tagName"].ToString().Equals("happy")){
                        messageBody.happyProbability = (double) prediction["probability"];
                    }

                    if (prediction["tagName"].ToString().Equals("sad"))
                    {
                        messageBody.sadProbability = (double) prediction["probability"];
                    }
                }
            }
        }
    }
}
