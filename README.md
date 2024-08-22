本项目是一些自建API，目前支持 [render](https://render.com) 、Docker 部署。

## Demo

https://awesome-api-mu5q.onrender.com

## API列表

| 名称     | 用途       | 备注     |
|--------|----------|--------|
| qrcode | 解析二维码    | 支持一图多码 |
| 极验     | 保存人机验证结果 |        |  

更多 API 文档 可访问 `/docs` 查看。

### qrcode

#### 以图片 URL 的形式

该接口还支持以下参数

|   字段    |   类型   | 描述          | 必要 |
|:-------:|:------:|:------------|:--:|
|   url   |  str   | 图片的链接       | Y  |
| headers | object | 访问URL使用的请求头 | N  |
| timeout |  int   | 请求超时时间      | N  |

```http request
POST http://localhost:8000/api/qrcode/url
Content-Type: application/json

{
   "url": "https://example.com/test.jpg"
}
```

#### 以图片文件的形式

```http request
POST http://localhost:8000/api/qrcode
Content-Type: multipart/form-data; boundary=WebAppBoundary

--WebAppBoundary
Content-Disposition: form-data; name="file"; filename="test.png"
Content-Type: multipart/form-data

< test.png
--WebAppBoundary--
```

#### 响应内容

```json5
{
  "code": 0,
  "message": "success",
  "data": [
    "测试内容",
    "https://example.com/"
  ]
}
```

## 部署

### Render 部署

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/BennettChina/awesome-api)


### Docker 部署

```shell
docker run -d \
--name awesome-api \
-p 8000:80 \
-e REDIS_HOST=localhost \
-e REDIS_PORT=6379 \
-e REDIS_PASSWORD=password \
bennettwu/awesome-api
```

### Docker Compose 部署

```yaml
version: "3"
services:
  awesome-api:
    image: awesome-api:latest
    container_name: awesome-api
    environment:
      REDIS_HOST: <redis ip>
      REDIS_PORT: <redis port>
      REDIS_PASSWORD: <redis password>
    ports:
      - "8000:80"
    restart: unless-stopped
```

### 源码部署

```shell
pip3 install -r requirements.txt && \
uvicorn api.index:app --host 0.0.0.0 --port 8000
```

## 环境变量

| 名称             | 描述 | 默认值         |
|----------------|----|-------------|
| REDIS_HOST     | IP | `localhost` |
| REDIS_PORT     | 端口 | `6379`      |
| REDIS_PASSWORD | 密码 |             |
| REDIS_DB       | DB | `0`         |
