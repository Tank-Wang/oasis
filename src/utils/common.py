from src.utils.log import get_logger

logger = get_logger(__name__)

def run_function_with_retry(func, max_retries=3, error_msg="Operation failed"):
    """
    使用重试机制运行函数
    
    Args:
        func: 要执行的函数（必须是无参数的callable）
        max_retries: 最大重试次数
        error_msg: 错误信息前缀
        
    Returns:
        函数执行结果，如果所有重试都失败则返回None
    """
    retry_count = 0
    while retry_count <= max_retries:
        result = func()
        if result:
            return result
            
        retry_count += 1
        if retry_count <= max_retries:
            logger.error(f"{error_msg}, retrying... ({retry_count}/{max_retries})")
        else:
            logger.error(f"{error_msg} after {max_retries} retries")
    
    return None
