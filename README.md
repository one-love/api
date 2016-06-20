One Love REST API
=================

[![Run Status](https://api.shippable.com/projects/5478a4b2d46935d5fbbee379/badge?branch=master)](https://app.shippable.com/projects/5478a4b2d46935d5fbbee379)
[![Stories in Ready](https://badge.waffle.io/one-love/backend.png?label=ready&title=Ready)](https://waffle.io/one-love/backend)

This is the API part of [One Love](https://one-love.github.io) based on Python Flask.

### Contributing

If you are intresting in contributing to this project, be sure to visit the [contributing page](https://github.com/one-love/one-love/doc/contributing.md). For easier development, take a look at [One Love Vagrant repository](https://github.com/one-love/vagrant-one-love).

### Usage
To get a login token:
```bash
curl -k -H 'Content-Type: application/json' -H 'Accept: application/json' http://onelove.vagrant:5000/api/v0/auth/tokens -X POST -d '{"email": "admin@example.com", "password": "Sekrit"}'



```
To use the token to get list of clusters:
```bash
curl -k -H 'Content-Type: application/json' -H 'Accept: application/json' -H 'Authorization: JWT <token>' http://onelove.vagrant:5000/api/v0/clusters
```

In the same way you can get other resorces/endpoints


### Swagger
To use swagger open [Swagger UI](http://onelove.vagrant:5000/api/v0/doc/)

