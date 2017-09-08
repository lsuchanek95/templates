
# How to use this template

```shell
heat stack-create -P keypair=your_keypair -f ./serverless.yaml serverless
```

After deployment, ssh to app_server and check `/var/log/cloud-init-output.log`, when you saw following at the end of file, custom script is finished.

```
Cloud-init v. 0.7.5 finished at Fri, 08 Sep 2017 08:04:10 +0000. Datasource DataSourceOpenStack [net,ver=2].  Up 142.16 seconds
```