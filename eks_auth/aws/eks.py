import yaml


def get_cluster_details(client, cluster_name):
    cluster = client.describe_cluster(name=cluster_name)
    cluster_cert = cluster["cluster"]["certificateAuthority"]["data"]
    cluster_ep = cluster["cluster"]["endpoint"]

    cluster_details = {}
    cluster_details['endpoint'] = cluster_ep
    cluster_details['cluster_cert'] = cluster_cert

    return cluster_details

def build_kube_config(cluster_name, cluster_details, account_number, role_arn, region):
    api_endpoint = cluster_details['endpoint']
    cert_authority = cluster_details['cluster_cert']
    cluster_arn = 'arn:aws:eks:' + region + ':' + account_number + ':cluster/' + cluster_name
    cluster_config = {
        "apiVersion": "v1",
        "kind": "Config",
        "clusters": [
          {
            "cluster": {
              "server": str(api_endpoint),
              "certificate-authority-data": str(cert_authority)
            },
            "name": str(cluster_arn),
          }
        ],
        "contexts": [
          {
            "context": {
              "cluster": str(cluster_arn),
              "user": str(cluster_arn)
            },
            "name": str(cluster_arn)
          }
        ],
        "current-context": str(cluster_arn),
        "preferences": {},
        "users": [
          {
            "name": str(cluster_arn),
            "user": {
              "exec": {
                "apiVersion": "client.authentication.k8s.io/v1alpha1",
                "command": "aws-iam-authenticator",
                "args": [
                  "token", "-i", str(cluster_name), "-r", str(role_arn)
                ]
              }
            }
          }
        ]
    }

    return cluster_config

def write_to_kube_config(kube_config):
    config_text = yaml.dump(kube_config, default_flow_style=False)
    open('./kube.config', "w").write(config_text)


def main(client, cluster_name, account_number, role_arn, region):
    cluster_details = get_cluster_details(client, cluster_name)
    kube_config = build_kube_config(
        cluster_name,
        cluster_details,
        account_number,
        role_arn,
        region
    )
    write_to_kube_config(kube_config)

if __name__ == '__main__':
    main()