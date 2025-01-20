from src.utils.log import get_logger

logger = get_logger(__name__)

def run_function_with_retry(func, max_retries=3, error_msg="Operation failed"):
    """
    Run function with retry mechanism
    
    Args:
        func: Function to execute (must be a callable without parameters)
        max_retries: Maximum number of retries
        error_msg: Error message prefix
        
    Returns:
        Function execution result, return None if all retries fail
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
