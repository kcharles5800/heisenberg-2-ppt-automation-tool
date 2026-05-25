# Heisenberg 2.0 (beta) : Automating Song Lyrics Presentations
***Streamlining church presentations:*** A Python-based automation tool to scrape song lyrics and generate formatted PowerPoint slide decks in seconds. Heisenberg 2.0 is a powerful, Python-based automation tool designed to generate song lyrics PowerPoint presentations effortlessly.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![PyQt6](https://img.shields.io/badge/PyQt6-41CD52?style=for-the-badge&logo=qt&logoColor=white) ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

## Overview
Heisenberg 2.0 was built to streamline the presentation creation process for church services. By automating the extraction of lyrics and the construction of slides, it removes the manual drudgery of formatting song presentations.

## Technical Stack

- **Backend**: Python, Selenium (Data Scraping), PyQt6 (GUI Framework)

- **Frontend**: HTML5/CSS3 (WebEngineView)

- **Packaging**: Inno Setup (Windows Installer)

## Key Features
- **Automated Extraction**: Scrapes lyrics directly from [Tamil Christian Songs](https://tamilchristiansongs.in/tamil/).

- **Smart UI**: A sleek, web-based interface that handles real-time status updates.

- **System Independent**: Fully portable design with registry-based configuration persistence.

- **Seamless Generation**: One-click PowerPoint creation with automatic file opening.

## Implementation Details
The process is split into two robust components:

1. **Data Scraping**: Utilizes Selenium to fetch lyrics. The system is designed to handle edge cases in web data, with modular code in data_scraping.py.

2. **Presentation Synthesis**: Orchestrates the creation of slides.

## Current Limitations & Roadmap
Language Support: This version (v2.0.1) is specialized for English-Tamil presentations. Expanding support to include a wide variety of additional languages is a primary focus for future updates.

### Stability: 

This tool is currently in ***Beta***. Please report any issues in the "Issues" tab.



> ## How to Install
> 1. Download the latest installer from the Releases page.
>
> 2. Run the ***heisenberg-2.0-setup.exe*** file.
>
> 3. The application will be automatically added to your Start Menu for easy access.

---

#### Developer: kcharles | [GitHub Profile](https://github.com/kcharles5800)
`Documentation: V1.0.2 // Build 012`
