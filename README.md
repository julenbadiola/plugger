[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/julenbadiola/plugger">
    <img src="app/apps/static/favicon/favicon.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Plugger</h3>

  <p align="center">
    An awesome README template to jumpstart your projects!
    <br />
    <a href="https://github.com/julenbadiola/plugger"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/julenbadiola/plugger/issues">Report Bug</a>
    ·
    <a href="https://github.com/julenbadiola/plugger/issues">Request Feature</a>
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

Plugger is a tool that allows you to quickly, easily, and customisably launch web services from a simple, authenticated user interface. It uses Docker's python SDK to interact with the underlying docker compose or docker swarm stack.

[![Plugger Screen Shot][plugger-screenshot]](https://example.com)


### Built With

* [Django](https://www.djangoproject.com/)
* [Docker Python SDK](https://pypi.org/project/docker/)




<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* Docker
* Docker compose

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/julenbadiola/plugger
   ```
2. Run the docker-compose
   ```sh
   make dev
   ```
   or

   ```sh
   docker-compose up -d -f docker-compose.dev.yml
   ```


<!-- USAGE EXAMPLES -->
## Usage

You can customize the plugins available by adding json files to the /plugins directory.


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/julenbadiola/plugger.svg?style=for-the-badge
[contributors-url]: https://github.com/julenbadiola/plugger/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/julenbadiola/plugger.svg?style=for-the-badge
[forks-url]: https://github.com/julenbadiola/plugger/network/members
[stars-shield]: https://img.shields.io/github/stars/julenbadiola/plugger.svg?style=for-the-badge
[stars-url]: https://github.com/julenbadiola/plugger/stargazers
[issues-shield]: https://img.shields.io/github/issues/julenbadiola/plugger.svg?style=for-the-badge
[issues-url]: https://github.com/julenbadiola/plugger/issues
[license-shield]: https://img.shields.io/github/license/julenbadiola/plugger.svg?style=for-the-badge
[license-url]: https://github.com/julenbadiola/plugger/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/julen-badiola-860191183/
[plugger-screenshot]: screenshot.png