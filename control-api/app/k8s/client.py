from kubernetes import client, config


def get_apps_v1_api():
    config.load_kube_config()
    return client.AppsV1Api()


def scale_deployment(name: str, replicas: int, namespace: str = "default"):
    api = get_apps_v1_api()
    body = {"spec": {"replicas": replicas}}
    api.patch_namespaced_deployment_scale(name=name, namespace=namespace, body=body)
    return {"deployment": name, "replicas": replicas}