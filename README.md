[![CodeQL](https://github.com/INRIM/service-app/workflows/CodeQL/badge.svg)](https://github.com/INRIM/service-app/actions?query=workflow%3ACodeQL "Code quality workflow status")
![Build status](https://img.shields.io/github/license/INRIM/service-app)
# Service App

Service App is a project and framework designed to

- RAD framework
- design form with formio builder and render with CRUD Api that implement
  italian [AGID Theme](https://github.com/italia/bootstrap-italia/)
- available plugin class system to build your own backend and/or frontend custom service
- documentation for plugin development is in WIP

Read the complete [Documentations ](docs/index.md)

### TODO

- i18n
- automated test
- FomIo component TODO list [available here](https://github.com/INRIM/service-app/blob/master/web-client/core/themes/italia/README.md)

## Features

- Design your form with Form.io builder for more info about Form.io see [Form.io homepage](https://www.form.io)
- View Form, the form is server side rendered with jinja template
- Add and Edit Data with yours forms
- MongoDB based
- And more

## Build Demo

- #### Config
  
    ```
    cp cfg_template/._env.template.demo .env
    cp cfg_template/template.demo.config.json config.json 
    ```

- #### Build and run
    ```
    ./deploy.sh
    ```

- #### app
    ```
     http://localhost:8526/
    ```
  open [Service App](http://localhost:8526/login/) in your browser 
  
- #### Login and usage
  
  -  When app start standard user is Public User.
  -  on upper rigth side of blue header bar click on "Public User" dropdown menu then logout
  -  Now you can login in app with:
     - user:  **admin**
     - password: **admin**

  - **Activate Builder mode**:
    - After login, on upper right side of blue header bar click "Admin Admin" dropdown
    - click on the **Builder** toggle 
    - Now the app is in builder mode, you can design forms, resources and edit other settings.
  
- ### Backend Api OSA3
 
  - [ReDoc](http://localhost:8225/redoc)


![Screen](gallery/form-design.png "Screen")

![Screen](gallery/form-design-json-logic.png "Screen")

![Screen](gallery/report-design.png "Screen")

![Screen](gallery/report-add-print-button.png "Screen")

![Screen](gallery/list-view-filter.png "Screen")

![Screen](gallery/export-xls.png "Screen")

![Screen](gallery/report-pdf-record.png "Screen")

## Docker Compose version

install/update docker compose from [Docker Compose Repo](https://github.com/docker/compose/releases)
mkdir -p ~/.docker/cli-plugins/
wget -O ~/.docker/cli-plugins/docker-compose https://github.com/docker/compose/releases/download/2.2.3/docker-compose-<SO>
chmod a+x ~/.docker/cli-plugins/docker-compose

## Dependencies:

* [FastApi](https://fastapi.tiangolo.com) - The Api framework
* [Form.io](https://www.form.io)
* [Jinja](https://github.com/pallets/jinja) - Jinja is a fast, expressive, extensible templating engine
* [AGID Theme](https://github.com/italia/bootstrap-italia/)
* [jQuery QueryBuilder](https://querybuilder.js.org/)
* [Redis](https://redis.io) - Used as Cache Service 
* [Cisco ClamAV](https://www.clamav.net) - Used in upload file as virus scanner Service

Authors
------------

- Alessio Gerace

## License

This project is covered by a [MIT license](https://github.com/INRIM/service-app/blob/master/LICENSE).