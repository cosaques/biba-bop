## APIs
* [vinted](https://www.vinted.fr/api/v2/catalog/items?search_text=t+shirt&page=1&catalog_ids=2050)
* CURL:
  * curl -X GET "https://www.vinted.fr/api/v2/catalog/items?search_text=t+shirt&page=1&catalog_ids=2050" \
-H "accept: application/json, text/plain, */*" \
-H "accept-encoding: identity" \
-H "accept-language: fr" \
-H "cookie: access_token_web=eyJraWQiOiJFNTdZZHJ1SHBsQWp1MmNObzFEb3JIM2oyN0J1NS1zX09QNVB3UGlobjVNIiwiYWxnIjoiUFMyNTYifQ.eyJhcHBfaWQiOjQsImNsaWVudF9pZCI6IndlYiIsImF1ZCI6ImZyLmNvcmUuYXBpIiwiaWF0IjoxNzM2NzQ0OTA0LCJzaWQiOiI4Y2IyODAxZC0xNzM2NTgyNzcwIiwic2NvcGUiOiJwdWJsaWMiLCJleHAiOjE3MzY3NTIxMDQsInB1cnBvc2UiOiJhY2Nlc3MifQ.ospxBI9rXLP-SThhJKBTvQ2bD3QxyrXj8XlHThXHjm4CHC4oz_xRNL-8x_aIjqrPwSB5o7ggpR6-OlswDxOcqO23feMF5d_d573lhXSobymedPjokaWxzcm8H-4bx04YsiaPs8yA5d7Rw5ManftbMlCPmxmqnyAu7ESTqOFyLGbBosEMyWR3w3ERkg2Db-K5xUk7_VSWMCNGD31ufQ5aa9YaofhY5lxcUTgIkB7zAA4QVZNlF_pl9cJdX_iZqvQGupNNM1QyESAcTqXrBXbVixledeYJri83E6SomAkUtEKnmaYq83y0oOsQu23amzXLXlym2emxIqcjUn9w6NOikQ" \
-H "referer: https://www.vinted.fr" \
-H "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36" \
--output -

## Resources
* [original project](https://github.com/phillipi/pix2pix)
  * [pytorch version](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix)
* [tutorial how img2img with tensorflow](https://www.tensorflow.org/tutorials/generative/pix2pix)
* [real time pix2pix turbo](https://huggingface.co/spaces/radames/real-time-pix2pix-turbo)

## Ideas
* ControlNet - I give for all images a silhouette of ideal t-shirt to control the generation.
