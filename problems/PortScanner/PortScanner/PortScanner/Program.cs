using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace PortScanner
{
    class Program
    {
        static void Main(string[] args)
        {
            ScannerArguments parsedArguments;
            if (!ScannerArguments.TryGetArguments(args, out parsedArguments))
                return;
            Logger.InitLogger();
            var scr = new Scanner();
            var ip = IPAddress.Parse(parsedArguments.IpAddress);
            var start = parsedArguments.StartPortsRange;
            var stop = parsedArguments.EndPortsRange;
            Task.WaitAll(scr.Scan(ip, start, stop));
        }
    }
}
