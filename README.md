本项目是一些自建API，目前支持 [vercel](https://vercel.com) 、Docker 部署。

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