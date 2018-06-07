using System;

class MessageBody
{
  public Machine drone { get; set; }
  public Ambient ambient { get; set; }
  public DateTime timeCreated { get; set; } = DateTime.Now;
}