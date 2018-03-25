using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Fclp;

namespace PortScanner
{
    class ScannerArguments
    {
        public string IpAddress { get; set; }
        public int StartPortsRange { get; set; }
        public int EndPortsRange { get; set; }

        public static bool TryGetArguments(string[] args, out ScannerArguments parsedArguments)
        {
            var argumentsParser = new FluentCommandLineParser<ScannerArguments>();
            argumentsParser.Setup(a => a.IpAddress)
                .As('a', "address")
                .Required();

            argumentsParser.Setup(a => a.StartPortsRange)
                .As('s', "start")
                .Required();

            argumentsParser.Setup(a => a.EndPortsRange)
                .As('e', "end")
                .Required();

            argumentsParser.SetupHelp("?", "h", "help")
                .Callback(text => Console.WriteLine(text));

            var parsingResult = argumentsParser.Parse(args);

            if (parsingResult.HasErrors)
            {
                argumentsParser.HelpOption.ShowHelp(argumentsParser.Options);
                parsedArguments = null;
                return false;
            }

            parsedArguments = argumentsParser.Object;
            return !parsingResult.HasErrors;
        }
    }
}
