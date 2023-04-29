<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/m_logo.png" alt="Logo">
  </a>

  <h3 align="center">VPyGUIGenerator</h3>

  <p align="center">
  A simple and useful library to help you create GUI for your application with just 1 line of code in Python
    <br />
    <br />
    <a href="https://www.youtube.com/watch?v=IYn2XRqFxt4&ab_channel=vrfEducation">Introduction Demo (Create GUI using fields</a>
    <br />
    <a href="https://www.youtube.com/watch?v=_OTW9OuXKjI&ab_channel=vrfEducation">Support property, customize widgets, New Widgets Demo</a>
    <br />
    <a href="https://www.youtube.com/watch?v=AMEmSsgtQCU&ab_channel=vrfEducation">Size support, List/Dict filtering, SimpleGrid Demo</a>
    <br />
    <a href="https://www.youtube.com/watch?v=7LRM_ksP8b8&ab_channel=vrfEducation">List/Dict ClearAll option, CRUD support in SimpleGrid</a>
    <br />
    <a href="https://www.youtube.com/watch?v=yBFSU8m3gdg&ab_channel=vrfEducation">Filtering option in SimpleGrid Demo</a>
    <br />
    ·
    <a href="https://github.com/vRFEducation/VPyFormGenerator/issues">Report Bug</a>
    ·
    <a href="https://github.com/vRFEducation/VPyFormGenerator/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>




<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]]
[![Product Name Screen Shot][product-screenshot2]]
[![Product Name Screen Shot][product-screenshot3]]
[![Product Name Screen Shot][product-screenshot4]]
[![Product Name Screen Shot][product-screenshot5]]
[![Product Name Screen Shot][product-screenshot6]]
[![Product Name Screen Shot][product-screenshot7]]


Creating GUI for Python application, in my opinion, is a tedious task and sometimes it's really hard to create and manage forms and dialogs inside an application. 
Although some library such as PyQt and PySide make it much easier to create GUI compare to TKinter, developers should create GUI using QtDesigner to write it completely in code. 
Most of the time we need to create a form to show current state of an object and let user modify the content(2-way binding).
This library will help us create GUI for objects with just writing 1 line of code. GUI created based on object fields and bindings also created. So user can see current state of object(as it's in the screenshot) 
and change the object state through that form.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* Python
* PyQt

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
Download and install Python on your machine
* pyqt
  ```sh
  pip install pyqt
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/vRFEducation/VPyFormGenerator
   ```
2. Create a class in your application such as:
   ```sh
  class Person:
    def __init__(self, name, age, height):
        self.name  = name
        self.age = age
        self.height = height
        self.is_male = True
        self.register_date = date.today()
        now = datetime.now()
        self.last_login = now
        self.break_time = now.time()
        self.courses = ["DB", "DS", "Python"]
        self.work_hours = {"Jan": 100, "Feb": 50, "Mar": 120}
    ```

3. Import the library:
   ```sh
    from  VPyFormGenerator.VPyGUIGenerator import VPyGUIGenerator
  ```
4. Create PyQt app and call create_gui method of library:
   ```sh
  import sys
  from PyQt6.QtWidgets import QApplication
  app = QApplication(sys.argv)
  dialog = VPyGUIGenerator.create_gui(p)
  dialog.show()
  app.exec()
```
5. Enjoy the dialog created!!!

   

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Most of the time Python developers use console for interacting with their application objects and it's totally a nightmare to create GUI for Python applications. This library will help developers create
simple and useful GUI for their application's objects in order to interact with them(view current state and change their values).
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Support propery inside Python classes
    - [ ] Customize default widgets for known types
- [ ] Add flatern option for complex objects
- [ ] Support PySide 

See the [open issues](https://github.com/vRFEducation/VPyFormGenerator/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



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

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Vahid Rahmanifard - rahmanifard@live.com

Project Link: [https://github.com/vRFEducation/VPyFormGenerator](https://github.com/vRFEducation/VPyFormGenerator)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/vRFEducation/VPyFormGenerator/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/vRFEducation/VPyFormGenerator/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/vRFEducation/VPyFormGenerator/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/vRFEducation/VPyFormGenerator/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/vRFEducation/VPyFormGenerator/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/vrahmanifard/
[product-screenshot]: images/m_screenshot.png
[product-screenshot2]: images/m_screenshot2.png
[product-screenshot3]: images/m_screenshot3.png
[product-screenshot4]: images/m_screenshot4.png
[product-screenshot5]: images/m_screenshot5.png
[product-screenshot6]: images/m_screenshot6.png
[product-screenshot6]: images/m_screenshot7.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
