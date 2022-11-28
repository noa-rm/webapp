from kubernetes import client, config
from kubernetes.client.rest import ApiException
import logging
import sys

from flask import Flask

app = Flask(__name__)

config.load_incluster_config()
core_v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()

Format = "%(asctime)s [%(levelname)s] %(message)s"
logging.basicConfig(format=Format, level=logging.INFO)
logger = logging.getLogger()


# list of namespaces in the cluster
@app.route("/namespaces")
def get_namespace_list():
    try:
        all_namespace = core_v1.list_namespace(watch=False).items
        all_namespace_lst = [ns.metadata.name for ns in all_namespace]
        logger.info(all_namespace_lst)
        return all_namespace_lst
    except ApiException as e:
        logger.error(f"Exception when calling CoreV1Api->list_namespace:{e}")
        sys.exit(1)


# list of services in a namespace
@app.route("/<string:ns>/services")
def get_namespaced_service_list(ns):
    try:
        ## check if ns exists in cluster
        namespaced_service = core_v1.list_namespaced_service(namespace=ns).items
        namespaced_service_lst = [svc.metadata.name for svc in namespaced_service]
        logger.info(namespaced_service_lst)
        return namespaced_service_lst
    except ApiException as e:
        logger.error(f"Exception when calling CoreV1Api->list_namespaced_service:{e}")
        sys.exit(1)


# list of deployments in a namespace
@app.route("/<string:ns>/deployments")
def get_namespaced_deployment_list(ns):
    try:
        namespaced_deployment = apps_v1.list_namespaced_deployment(namespace=ns).items
        namespaced_deployment_lst = [dep.metadata.name for dep in namespaced_deployment]
        logger.info(f"Namespace={ns}, Deployments list={namespaced_deployment_lst}")
        return namespaced_deployment_lst
    except ApiException as e:
        logger.error(
            f"Exception when calling AppsV1Api->list_namespaced_deployment:{e}"
        )


def get_deployment_labels_list(deployment_name, namespace):
    try:
        namespaced_deployment = apps_v1.read_namespaced_deployment(
            name=deployment_name, namespace=namespace
        )
        dep_labels = [
            f"{k}={v}"
            for k, v in namespaced_deployment.spec.selector.match_labels.items()
        ]
        return dep_labels
    except ApiException as e:
        logger.error(f"Exception when calling CoreV1Api->list_namespaced_pod:{e}")
        sys.exit(1)


# list of pods in a deployment in a namespace
@app.route("/<string:ns>/<string:deploy>/pods")
def get_namespaced_deployments_pod_list(ns, deploy):
    try:
        labels_lst = get_deployment_labels_list(namespace=ns, deployment_name=deploy)
        labels = ", ".join(labels_lst)
        namespaced_deployment_pods = core_v1.list_namespaced_pod(
            namespace=ns, label_selector=labels
        ).items
        namespaced_deployments_pods_lst = [
            dep_pod.metadata.name for dep_pod in namespaced_deployment_pods
        ]
        logger.info(
            f"namespaced_deployment_pods={namespaced_deployments_pods_lst}, Deployment={deploy}, Namespace={ns}"
        )
        return namespaced_deployments_pods_lst
    except ApiException as e:
        logger.error(f"Exception when calling CoreV1Api->list_namespaced_pod:{e}")
        sys.exit(1)


@app.route("/")
def index():
    return "Hello from Noa's simple web app!"


if __name__ == "__main__":
    logger.info("Launching noa-web-app...")
    app.run(host="0.0.0.0", debug=False, port=5000)
