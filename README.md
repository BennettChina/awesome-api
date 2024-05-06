本项目是一些自建API，目前支持 [render](https://render.com) 、Docker 部署。

## Demo

https://awesome-api-mu5q.onrender.com

## API列表

| 名称     | 用途    | 备注     |
|--------|-------|--------|
| qrcode | 解析二维码 | 支持一图多码 |

- qrcode

```http request
### 以图片链接的形式
GET localhost:8000/api/qrcode?url={image_url}
```

```http request
### 以图片文件的形式
POST localhost:8000/api/qrcode
Content-Type: multipart/form-data; boundary=WebAppBoundary

--WebAppBoundary
Content-Disposition: form-data; name="file"; filename="test.png"
Content-Type: multipart/form-data

< test.png
--WebAppBoundary--
```

## 部署

### Docker 部署

```shell
docker run -d --name awesome-api -p 8000:80 bennettwu/awesome-api
```

### Docker Compose 部署

```yaml
version: "3"
services:
  awesome-api:
    image: awesome-api:latest
    container_name: awesome-api
    ports:
      - "8000:80"
    restart: unless-stopped
```

### 源码部署

```shell
pip3 install -r requirements.txt && \
uvicorn api.index:app --host 0.0.0.0 --port 8000
```