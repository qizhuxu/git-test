import requests
import asyncio
import aiohttp
import json
from typing import List, Dict, Optional
import re

# API Keys 配置
RAW_KEYS_MULTI_LINE = """
fk-Q3xngb7A6qmqAee2HqVW-ymCH3CdX2QMCLTI_bbDRfyPEWzXsYyj2CmSFCRWbCcc
fk-9G6vF8RRsB5MAm3pbJQx-tjCGrHhUauVhdA9lyEtrfOKox9laNj8yeXPY42whQ6E
fk-PR4RprQMmDOHmOEbGKdV-01G1AJBZBnufHAvW927YTpGbqU_AjK86hTwcyTAI-yc
fk-UPNO8p3ni2N75VOnP9Ki-AaeLC6xzhTwJN2xEsenjWzsfMASC_0uVbQ5cqNf2Oew
fk-DnBPYsuVUYFPYOnXesYn-pURFmuMunj6_jR6xmIQWblvlWXHQOeNwgAxD8RltyJc
fk-s6Q8796pDw0en62bo2we-xsd8Y4O6S1LUaWsYYyUHoEqoF2SKZtI2CthD2pv0RkA
fk-CsyaSNwPidsi16zAqTB5-8eqCT8OVynAplAAIsbEwXl6i9Ta2Rpp8J_7TgksD5t4
fk-nkVfjGZnQDu8gMckgzjm-mNYnMgUHMZvANEHo4CkDlY_Xnm7xSej3TaJ3ZCiLKNc
fk-I7oc2scuPxjCBj3hSzYW-Nz5NvWmu8vec7_FuoKj-CSJzVznc1e_M6MAsQAixpQg
"""

def sanitize_key(key: str) -> str:
    """清理 API 密钥，移除空白字符和非 ASCII 字符"""
    if not key:
        return ""
    # 移除所有空白字符
    cleaned = re.sub(r'\s+', '', key).strip()
    # 移除非 ASCII 可打印字符
    cleaned = re.sub(r'[^\x20-\x7E]', '', cleaned)
    return cleaned

def is_valid_key(key: str) -> bool:
    """验证密钥是否只包含有效的 ASCII 字符"""
    if not key:
        return False
    return bool(re.match(r'^[\x20-\x7E]+$', key))

def parse_keys() -> List[str]:
    """解析和处理 API 密钥"""
    keys = []
    for line in RAW_KEYS_MULTI_LINE.strip().split('\n'):
        cleaned_key = sanitize_key(line)
        if cleaned_key and is_valid_key(cleaned_key):
            keys.append(cleaned_key)
    return keys

class FactoryAIChecker:
    def __init__(self):
        self.base_url = "https://app.factory.ai"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
        }
    
    async def check_single_key_async(self, session: aiohttp.ClientSession, key: str, index: int) -> Dict:
        """异步检查单个 API 密钥的余额"""
        try:
            headers = self.headers.copy()
            headers['Authorization'] = f'Bearer {key}'
            
            async with session.get(
                f"{self.base_url}/api/organization/members/chat-usage",
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                
                if response.status != 200:
                    return {
                        'key': key,
                        'index': index,
                        'error': f'HTTP {response.status}'
                    }
                
                data = await response.json()
                
                if not data.get('usage') or not data['usage'].get('standard'):
                    return {
                        'key': key,
                        'index': index,
                        'error': 'Invalid response structure'
                    }
                
                standard_usage = data['usage']['standard']
                total_allowance = standard_usage.get('totalAllowance', 0)
                org_total_tokens_used = standard_usage.get('orgTotalTokensUsed', 0)
                remaining = total_allowance - org_total_tokens_used
                
                return {
                    'key': key,
                    'index': index,
                    'totalAllowance': total_allowance,
                    'orgTotalTokensUsed': org_total_tokens_used,
                    'remaining': remaining
                }
                
        except asyncio.TimeoutError:
            return {'key': key, 'index': index, 'error': 'Request timeout'}
        except aiohttp.ClientError as e:
            return {'key': key, 'index': index, 'error': f'Network error: {str(e)}'}
        except json.JSONDecodeError:
            return {'key': key, 'index': index, 'error': 'JSON parse error'}
        except Exception as e:
            return {'key': key, 'index': index, 'error': f'Unexpected error: {str(e)}'}

    def check_single_key_sync(self, key: str, index: int) -> Dict:
        """同步检查单个 API 密钥的余额"""
        try:
            headers = self.headers.copy()
            headers['Authorization'] = f'Bearer {key}'
            
            response = requests.get(
                f"{self.base_url}/api/organization/members/chat-usage",
                headers=headers,
                timeout=30
            )
            
            if response.status_code != 200:
                return {
                    'key': key,
                    'index': index,
                    'error': f'HTTP {response.status_code}'
                }
            
            data = response.json()
            
            if not data.get('usage') or not data['usage'].get('standard'):
                return {
                    'key': key,
                    'index': index,
                    'error': 'Invalid response structure'
                }
            
            standard_usage = data['usage']['standard']
            total_allowance = standard_usage.get('totalAllowance', 0)
            org_total_tokens_used = standard_usage.get('orgTotalTokensUsed', 0)
            remaining = total_allowance - org_total_tokens_used
            
            return {
                'key': key,
                'index': index,
                'totalAllowance': total_allowance,
                'orgTotalTokensUsed': org_total_tokens_used,
                'remaining': remaining
            }
            
        except requests.Timeout:
            return {'key': key, 'index': index, 'error': 'Request timeout'}
        except requests.RequestException as e:
            return {'key': key, 'index': index, 'error': f'Network error: {str(e)}'}
        except json.JSONDecodeError:
            return {'key': key, 'index': index, 'error': 'JSON parse error'}
        except Exception as e:
            return {'key': key, 'index': index, 'error': f'Unexpected error: {str(e)}'}

async def check_keys_async(keys: List[str]) -> List[Dict]:
    """异步批量检查所有密钥"""
    checker = FactoryAIChecker()
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for index, key in enumerate(keys):
            task = checker.check_single_key_async(session, key, index)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        return results

def check_keys_sync(keys: List[str]) -> List[Dict]:
    """同步批量检查所有密钥"""
    checker = FactoryAIChecker()
    results = []
    
    for index, key in enumerate(keys):
        result = checker.check_single_key_sync(key, index)
        results.append(result)
        # 添加延迟避免请求过快
        import time
        time.sleep(0.1)
    
    return results

def print_results(results: List[Dict], keys_with_balance: List[Dict]):
    """打印结果"""
    print("=" * 80)
    print(f"检查完成！共 {len(results)} 个 keys，有余额的 keys: {len(keys_with_balance)} 个")
    print("=" * 80)
    
    if keys_with_balance:
        print('\n有余额的 API Keys:\n')
        for idx, item in enumerate(keys_with_balance, 1):
            print(f"{idx}. {item['key']}")
            print(f"   剩余额度: {item['remaining']:,} / {item['totalAllowance']:,}")
            print()
    else:
        print('\n没有找到有余额的 API Keys\n')
    
    # 统计信息
    valid_results = [r for r in results if 'error' not in r]
    total_allowance = sum(r.get('totalAllowance', 0) for r in valid_results)
    total_used = sum(r.get('orgTotalTokensUsed', 0) for r in valid_results)
    total_remaining = sum(r.get('remaining', 0) for r in valid_results)
    
    print("=" * 80)
    print("统计信息:")
    print(f"总额度: {total_allowance:,}")
    print(f"已使用: {total_used:,}")
    print(f"剩余: {total_remaining:,}")
    if total_allowance > 0:
        usage_rate = (total_used / total_allowance) * 100
        print(f"使用率: {usage_rate:.2f}%")
    print("=" * 80)

async def main_async():
    """异步主函数"""
    keys = parse_keys()
    print(f"\n开始检查 {len(keys)} 个 API keys...\n")
    
    results = await check_keys_async(keys)
    
    # 筛选有余额的 keys
    keys_with_balance = [
        r for r in results 
        if 'error' not in r and r.get('remaining', 0) > 0
    ]
    
    print_results(results, keys_with_balance)

def main_sync():
    """同步主函数"""
    keys = parse_keys()
    print(f"\n开始检查 {len(keys)} 个 API keys...\n")
    
    results = check_keys_sync(keys)
    
    # 筛选有余额的 keys
    keys_with_balance = [
        r for r in results 
        if 'error' not in r and r.get('remaining', 0) > 0
    ]
    
    print_results(results, keys_with_balance)

if __name__ == "__main__":
    # 安装依赖: pip install requests aiohttp
    
    # 方法1: 使用异步版本（推荐，速度更快）
    print("使用异步版本检查...")
    asyncio.run(main_async())
    
    # 方法2: 使用同步版本（更简单）
    # print("使用同步版本检查...")
    # main_sync()