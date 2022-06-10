<!--
SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
SPDX-License-Identifier: MPL-2.0
-->
# Kubernetes Konserver
Konserver is a Kubernetes controller that protects objects from deletion based
on dependencies defined in annotations.

## Usage
Install the controller using helm:
```shell
helm repo add magenta https://chartmuseum.magentahosted.dk
helm upgrade --install konserver magenta/konserver --namespace konserver
```

Set the `conservable` annotation on objects to protect from deletion. This
annotation is required so the controller doesn't add its finalizer to every
watched resource.
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: foo
  annotations:
    konserver.magenta.dk/conservable: "yes"
```

Then add the `conserve` annotation to another object, referencing the `foo`
ConfigMap. This ensures that `foo` cannot be deleted while `bar` exists.
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: bar
  annotations:
    konserver.magenta.dk/conserve: "configmaps.v1/foo,configmaps.v1/bar"
```


## Development
```shell
kopf run --standalone --namespace='*' --dev --verbose -m konserver.main
```
