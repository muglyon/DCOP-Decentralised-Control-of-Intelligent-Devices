using System;

class MessageBody
{
  // public Machine drone { get; set; }
  // public Ambient ambient { get; set; }
  public DateTime timeCreated { get; set; } = DateTime.Now;
  public double happyProbability { get; set; }
  public double sadProbability { get; set; }
}