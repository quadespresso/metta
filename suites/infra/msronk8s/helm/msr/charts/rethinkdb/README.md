# RethinkDB Helm Chart

## Prerequisites Details
* Kubernetes 1.19+.
* Persistent volume support on the underlying infrastructure.

## StatefulSet Details
* https://kubernetes.io/docs/concepts/abstractions/controllers/statefulsets/

## StatefulSet Caveats
* https://kubernetes.io/docs/concepts/abstractions/controllers/statefulsets/#limitations

## Acknowledgment of Previous Works

This chart was based on the official Helm chart at:
https://github.com/helm/charts/tree/b8725a14d3cffcaa4c9a4b3a88dd79a318335a8f/stable/rethinkdb

## Chart Details

This chart implements a dynamically scalable [RethinkDB Cluster](https://www.rethinkdb.com/docs/sharding-and-replication/) using Kubernetes StatefulSets.

## Installing the Chart

To install the chart with the release name `my-release`:

```console
$ helm install --name my-release stable/rethinkdb
```

## Configuration

The following table lists the configurable parameters of the rethinkdb chart and their default values.

Parameter | Description | Default
---|---|---
`image.repository` | Custom RethinkDB image repository | `rethinkdb-base`
`image.namespace` | Custom RethinkDB image repository namespace | `mirantiseng`
`image.tag` | Custom RethinkDB image tag | `2.3.6-mirantis-1`
`image.pullPolicy` | Custom RethinkDB image pull policy | `IfNotPresent`
`image.pullSecret` | Name of a stored secret containing image pull credentials if the image repo requires authentication | `undefined`
`nodeSelector` | Standard [nodeSelector](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#nodeselector) for restricting which nodes can run pods for this service | `{}`
`cluster.replicas` | Number of RethinkDB Cluster replicas | `3`
`cluster.resources` | Resource configuration for each RethinkDB Cluster Pod | `{}`
`cluster.podAnnotations` | Annotations to be added to RethinkDB Cluster Pods | `{}`
`cluster.service.annotations` | Annotations to be added to RethinkDB Cluster Service | `{}`
`cluster.storageClass.enabled` | If `true`, create a StorageClass for the cluster. **Note**: You must set a provisioner | `false`
`cluster.storageClass.provisioner` | Provisioner definition for StorageClass | `undefined`
`cluster.storageClass.parameters` | Parameters for StorageClass | `undefined`
`cluster.persistentVolume.enabled` | If `true`, persistent volume claims are created | `true`
`cluster.persistentVolume.storageClass` | Persistent volume storage class | `default`
`cluster.persistentVolume.accessMode` | Persistent volume access modes | `[ReadWriteOnce]`
`cluster.persistentVolume.size` | Persistent volume size | `1Gi`
`cluster.persistentVolume.annotations` | Persistent volume annotations | `{}`
`cluster.rethinkCacheSize` | RethinkDB `cache-size` value in MB | `100`
`cluster.clusterTLS.enabled` | Enables TLS on the intra-cluster connections. **Note**: If enabled, you must provide a key and certificates either through 'clusterTLS.secretName' or through 'clusterTLS.key', 'clusterTLS.cert', and 'clusterTLS.cacert' | `false`
`cluster.clusterTLS.secretName` | Name of a stored secret of type kubernetes.io/tls from which data fields 'tls.crt', 'tls.key', and 'ca.crt' will be utilized for TLS; if used with 'clusterTLS.key', 'clusterTLS.cert,' and 'clusterTLS.cacert', a stored secret by this name will be created using those values | `<CHART_NAME>-cluster-tls`
`cluster.clusterTLS.key` | Private key for cluster TLS | `undefined`
`cluster.clusterTLS.cert` | Certificate for cluster TLS | `undefined`
`cluster.clusterTLS.cacert` | CA certificate bundle for cluster cert validation | `undefined`
`proxy.replicas` | Number of RethinkDB Proxy replicas | `1`
`proxy.resources` | Resource configuration for each RethinkDB Proxy Pod | `{}`
`proxy.podAnnotations` | Annotations to be added to RethinkDB Proxy Pods | `{}`
`proxy.service.type` | RethinkDB Proxy Service Type | `ClusterIP`
`proxy.service.annotations` | Annotations to be added to RethinkDB Cluster Service | `{}`
`proxy.service.clusterIP` | Internal controller proxy service IP | `""`
`proxy.service.externalIPs` | Controller service external IP addresses | `[]`
`proxy.service.loadBalancerIP` | IP address to assign to load balancer (if supported) | `""`
`proxy.service.loadBalancerSourceRanges` | List of IP CIDRs allowed access to load balancer (if supported) | `[]`
`proxy.driverTLS.enabled` | Enables TLS on the driver connection. **Note**: If enabled, you must provide a key and certificate either through 'driverTLS.secretName' or through 'driverTLS.key' and 'driverTLS.cert' | `false`
`proxy.driverTLS.secretName` | Name of a stored secret of type kubernetes.io/tls from which data fields 'tls.crt' and 'tls.key' will be utilized for TLS; if used with 'driverTLS.key' and 'driverTLS.cert', a stored secret by this name will be created using those values | `<CHART_NAME>-driver-tls`
`proxy.driverTLS.key` | Private key for driver TLS | `undefined`
`proxy.driverTLS.cert` | Certificate for driver TLS | `undefined`
`proxy.driverTLS.mutual.secretName` | [optional] Name of a stored secret from which data field 'ca.crt' will be used to validate clients | `<CHART_NAME>-driver-tls-mutual`
`proxy.driverTLS.mutual.cert` | [optional] CA certificate bundle for client validation | `undefined`
`ports.cluster` | RethinkDB Cluster Port | `29015`
`ports.driver` | RethinkDB Driver Port | `28015`
`ports.admin` | RethinkDB Admin Port | `8080`
`rethinkdbPassword` | Password for the RethinkDB Admin user | `rethinkdb`

Specify each parameter using the `--set key=value[,key=value]` argument to `helm install`.

Alternatively, a YAML file that specifies the values for the parameters can be provided while installing the chart. For example,

```console
$ helm install --name my-release -f values.yaml stable/rethinkdb
```

> **Tip**: You can use the default [values.yaml](values.yaml)

## Important: Admin Password Management ##

The initial admin password is set by the config value `rethinkdbPassword`.  This value is also used by the probe which periodically checks if the RethinkDB Cluster and Proxy are still running.  If you change the RethinkDB admin password via a query (i.e. `r.db('rethinkdb').table('users').update({password: 'new-password'})`) this will cause the probe to fail which then restarts the pods over and over.  To stablize the cluster, you also need to use `helm upgrade` to update the password in the Kubernetes Secrets storage by doing:
```console
$ helm upgrade --set rethinkdbPassword=new-password my-release stable/rethinkdb
```

## Opening Up the RethinkDB Admin Console

The admin port is not available outside of the cluster for security reasons. The only way to access the admin console is to use a [Kubernetes Proxy](https://kubernetes.io/docs/concepts/cluster-administration/access-cluster/#manually-constructing-apiserver-proxy-urls). To open up the admin console:
```console
$ kubectl proxy
Starting to serve on 127.0.0.1:8001
```
Then use the following URL: http://localhost:8001/api/v1/namespaces/NAMESPACE/services/RELEASE_NAME-rethinkdb-admin/proxy
Make sure a replace `NAMEPSPACE` with the correct namespace and `RELEASE_NAME` that was used when installing the chart.

And then open up your browser to http://localhost:8080 and you should see the admin console

## Cleanup orphaned Persistent Volumes

Deleting a StatefulSet will not delete associated Persistent Volumes.

Do the following after deleting the chart release to clean up orphaned Persistent Volumes.

```console
$ kubectl delete pvc -l release=my-release
```

## Failover

If any RethinkDB server fails it gets re-joined eventually.
You can test the scenario by killing process of one of the pods:
```console
$ kubectl get pods -l release=my-release
NAME                                          READY     STATUS    RESTARTS   AGE
my-release-rethinkdb-cluster-0                1/1       Running   0          1m
my-release-rethinkdb-cluster-1                1/1       Running   0          2m
my-release-rethinkdb-cluster-2                1/1       Running   0          2m
my-release-rethinkdb-proxy-2517940628-81dxd   1/1       Running   1          1m

$ kubectl exec -it my-release-rethinkdb-cluster-0 -- ps aux | grep 'rethinkdb'
root         7  0.1  2.1 233496 43408 ?        Ssl  16:56   0:00 rethinkdb --ser
root        26  0.0  0.4 146948  8204 ?        S    16:56   0:00 rethinkdb --ser
root       100  0.0  0.7 157192 16060 ?        S    16:56   0:00 rethinkdb --ser

$ kubectl exec -it my-release-rethinkdb-cluster-0 -- kill 7
```

## Scaling

Scaling should be managed by `helm upgrade`, which is the recommended way. Example:
```
$ helm upgrade --set cluster.replicas=4 my-release stable/rethinkdb
```
