import sys, os
from subprocess import Popen, PIPE
sys.path.append(os.getcwd()+"/..")
from utils import DeploymentWriter

class ServerDeploymentWriter(DeploymentWriter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _replace_placeholders(self, config, name, text):
        text = text.replace("SITE_PLACEHOLDER", self._get_site_name(config))
        text = text.replace("NODE_PLACEHOLDER", config["node"])
        text = text.replace("NAME_PLACEHOLDER", name)
        text = text.replace("REDI_IPV6_PLACEHOLDER", config["redi_ipv6"])
        text = text.replace("REDI_PORT_PLACEHOLDER", config["redi_port"])
        text = text.replace("INTF_PLACEHOLDER", config["interface"])
        text = text.replace("PORT_PLACEHOLDER", config["port"])
        text = text.replace("IPV6_PLACEHOLDER", config["ipv6"])
        text = text.replace("HOST_DIR_PLACEHOLDER", config["host_dir"])
        return text

    def _get_deployment_name(self, config):
        N = config["node"].split(".")[0].split("-")[-1]
        return f"{self.app_name}-{N}-{config['port'].replace('.', '-')}"

    def _get_site_name(self, config):
        ipv6_last4 = config["ipv6"].split(":")[-1]
        return f"RUCIO_SENSE_SERVER_{ipv6_last4}_{config['port']}"

    def make_certs(self):
        if len(self._get_deployments()) == 0:
            print("WARNING: No certs made; run write() first!")
            return
        for config in self.configs:
            base_dir = f"{os.getcwd()}/{self.deployment_dir}/{self._get_deployment_name(config)}"
            cmd = f"../certs/generate.sh {config['ipv6']} {base_dir}"
            Popen(cmd.split(), cwd="../certs", stdout=PIPE).communicate()

if __name__ == "__main__":
    server_configs = [
        # Cluster 1
        {
            "node": "nrp-02.nrp-nautilus.io", 
            "ipv6": "2001:48d0:3001:111::300",
            "port": "2094",
            "interface": "macvlan0",
            "redi_ipv6": "2001:48d0:3001:111::200",
            "redi_port": "9001",
            "host_dir": "/tmp"
        }, 
        {
            "node": "nrp-02.nrp-nautilus.io", 
            "ipv6": "2001:48d0:3001:112::300",
            "port": "2095",
            "interface": "macvlan1",
            "redi_ipv6": "2001:48d0:3001:112::200",
            "redi_port": "9002",
            "host_dir": "/tmp"
        }, 
        {
            "node": "nrp-02.nrp-nautilus.io", 
            "ipv6": "2001:48d0:3001:113::300",
            "port": "2096",
            "interface": "macvlan2",
            "redi_ipv6": "2001:48d0:3001:113::200",
            "redi_port": "9003",
            "host_dir": "/tmp"
        }, 
    ]
    deployment_writer = ServerDeploymentWriter(
        base_dir="./", 
        template_dir="templates", 
        app_name="rucio-sense-server", 
        configs=server_configs
    )
    deployment_writer.write()
    deployment_writer.make_certs()
