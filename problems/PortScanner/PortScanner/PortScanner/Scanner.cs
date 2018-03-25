using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.NetworkInformation;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using log4net;

namespace PortScanner
{
    public class Scanner
    {
        private static readonly ILog log = Logger.Log;

        public int Timeout => 2000;
        private async Task<PortInfo> ScanTcpPortAsync(IPAddress address, int port, CancellationToken ct)
        {
            //Console.WriteLine($"===> Start scanning TCP port {port}");
            using (var client = new TcpClient())
            {
                var portInfo = new PortInfo(port, Protocol.TCP);
                var connection = client.ConnectAsync(address, port);

                if (await Task.WhenAny(connection, Task.Delay(Timeout, ct)) == connection && connection.Exception != null)
                    portInfo.Status = PortStatus.Close;
                else
                {
                    // Timeout occurred, this means that there is no connection and port is closed
                    portInfo.Status = PortStatus.Open;
                }
                return portInfo;
            }
        }

        private async Task<PortInfo> ScanUdpPortAsync(IPAddress address, int port, CancellationToken ct)
        {
            //Console.WriteLine($"===> Start scanning UDP port {port}");
            var portInfo = new PortInfo(port, Protocol.UDP);
            using (var udpClient = new UdpClient())
            {
                try
                {
                    udpClient.Connect(address, port);
                    udpClient.Client.ReceiveTimeout = Timeout;
                    var message = Encoding.ASCII.GetBytes("Are you open?");
                    udpClient.Send(message, message.Length);
                    var result = udpClient.ReceiveAsync();
                    if (await Task.WhenAny(result, Task.Delay(Timeout, ct)) == result)
                        Console.WriteLine(Encoding.ASCII.GetString(result.Result.Buffer));                        
                    portInfo.Status = PortStatus.Open;
                }
                catch (SocketException e)
                {
                    log.InfoFormat($"Error Code: {e}");
                    portInfo.Status = e.ErrorCode == 10054 || e.ErrorCode == 11001 
                        ? PortStatus.Close 
                        : PortStatus.Open;
                }
                return portInfo;
            }
        }

        public async Task Scan(IPAddress ipdAddress, int startPort, int endPort)
        {
            log.InfoFormat("=================\n\rStart scanning");
            CancellationTokenSource cancelTokenSource = new CancellationTokenSource();
            CancellationToken token = cancelTokenSource.Token;
            for (var port = startPort; port <= endPort; port++)
            {
                var output = new StringBuilder($"{port}: ");
                var tcpPortInfo = await ScanTcpPortAsync(ipdAddress, port, token);
                output.Append($"TCP {tcpPortInfo.Status}, ");
                var udpPortInfo = await ScanUdpPortAsync(ipdAddress, port, token);
                output.Append($"UDP {udpPortInfo.Status}");
                if (tcpPortInfo.Status == PortStatus.Open || udpPortInfo.Status == PortStatus.Open)
                    Console.WriteLine(output);
                log.InfoFormat(output.ToString());
            }
            log.InfoFormat("Stop scanning");
        }

    }   
}
