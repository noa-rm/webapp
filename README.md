# Noa's webapp
This project demonstrate usage of python webapp deployed on K8S cluster.
Project consists of python app and a helm chart to consume and deploy it over the environment.

#### Pre-requisites
* Image is locally built (configure tag in values.yaml)
* K8S cluster

#### Install
```bash
helm install <release-name> $PWD/noa-web-app
```

#### Usage
Fill in your input where `<>` is stated
* list of namespaces in the cluster:
```bash
curl http://<service-name>.default.svc.cluster.local/namespaces
```
* list of services in a namespace
```bash
curl http://<service-name>.default.svc.cluster.local/<namespace>/services
```
* list of deployments in a namespace
```bash
curl http://<service-name>.default.svc.cluster.local/<namespace>/deployments
```
* list of pods in a deployment in a namespace
```bash
curl http://<service-name>.default.svc.cluster.local/<namespace>/<deployment-name>/pods
```

#### Availability and Scalability
Implemented as a part of chart;
* Standard rolling deployment strategy
* HPA using [Metrics Server](https://github.com/kubernetes-sigs/metrics-server)

#### Testing Workloads
```bash
kubectl run -i --tty load-generator --rm --image=yauritux/busybox-curl:latest --restart=Never -- /bin/sh -c "while sleep 0.0001; do curl http://<service-name>.default.svc.cluster.local/<namespace>/<deployment-name>/pods; done"
```

#### Notes
* Deployed over `default` namespace
* Readiness probes were not configured
