# ImageSteganography

## Intro
Image steganography is a technique of hiding information within an image.\
The process involves embedding secret data within the image in such a way that it is not easily detectable to an observer.\
The goal is to hide the existence of the information by making it appear as if the image is unchanged.

The most common technique is called LSB (Least Significant Bit) steganography.\
In this method, the information is hidden by replacing the least significant bit of each pixel in the image with a bit of the secret data.

## Description
This project allows to encode and decode secret messages into and from images.


## The Slack Bot -
   Is the User Interface.

  * To encrypt a secret message into an image, send a Slack message. The message should follow these rules:
    * The message should be sent only in the Slack channel ID of which should be set in config.yaml file.
    * The message should begin with mentioning the bot and then the message to encrypt.
    * One image should be attached.
    * After the message will be sent, the image will be encrypted with the hidden message and stored.
  * To decipher images that are stored, use the Slack slash-command. In the command specify the manes of the images
  `/decipher <image_name_1> <image_name_2>...<<image_name_N>`


### Requirements
* A Linux Ubuntu Host Machine
* For the slack bot:
  * SLACK_APP_TOKEN
  * SLACK_BOT_TOKEN
  * BOT_ID
  * SLACK_CHANNEL_ID
* For the application:
  * A makenvfile  - will store the following Environment variables:
    1. SLACK_APP_TOKEN=<APP_TOKEN>
    2. SLACK_BOT_TOKEN=<BOT_TOKEN>
    3. BOT_ID=<BOT_ID>
  * An empty user_images.json file - will be mounted to the docker and will store the encrypted images. 
  The format of each entry: `{"name":<name_of_the_image>,"image":<image-a 3D array represents the image in RGB color>}`


### Install
1. Install the Slack Bot
2. Install the application
   1. Create a makenvfile should contain the following Environment variables:
      1. SLACK_APP_TOKEN=<APP_TOKEN>
      2. SLACK_BOT_TOKEN=<BOT_TOKEN>
      3. BOT_ID=<BOT_ID>
   2. Create an empty user_images.json - will be mounted to the volume and will store records about the images
   3. Open the Terminal
   4. docker pull ilya1200/image_steganography:v1.0.0
   5. docker run --name <CUSTOM_NAME_FOR_THE_CONTAINER> -p 3000:3000 --env-file <PATH_TO_makenvfile> -v <PATH_TO_user_images.json>:/app/ImageSteganographyServer/storage/user_images.json -d ilya1200/image_steganography:v1.0.0


### Usage
