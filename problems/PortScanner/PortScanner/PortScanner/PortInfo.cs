using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PortScanner
{
    public enum Protocol
    {
        TCP,
        UDP,
    }

    public enum PortStatus
    {
        NonDefined,
        Open,
        Close,
    }

    public class PortInfo
    {
        public int PortNumber { get; set; }
        public Protocol Protocol { get; set; }
        public PortStatus Status { get; set; }

        public PortInfo(int i, Protocol protocol)
        {
            PortNumber = i;
            Protocol = protocol;
        }
    }
}
