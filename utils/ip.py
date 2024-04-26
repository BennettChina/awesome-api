async def get_client_ip(request) -> str:
    """
    获取客户端的真实IP
    :param request: 请求对象
    :return: IP
    """
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    x_real_ip = request.headers.get('X-Real-IP')
    if x_real_ip:
        return x_real_ip
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
        return ip
    return request.client.host
