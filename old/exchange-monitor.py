import os
from threading import Timer
from uniswap import Uniswap

infura_url = "https://mainnet.infura.io/v3/163e368fa52d4fe39ed32f3f8635f6ce"
os.environ["PROVIDER"] = infura_url

# --- Tokens ---
ETH_ADDR = "0x0000000000000000000000000000000000000000"
SDT_ADDR = "0x73968b9a57c6E53d41345FD57a6E6ae27d6CDB2F"
ETH_DECIMALS = 10**18
SDT_DECIMALS = 10**18
eth_tokens = 1 * ETH_DECIMALS
sdt_tokens = 1 * SDT_DECIMALS

# --- Uniswap and SushiSwap wrappers ---
# Change if you are making transactions
address = "0x0000000000000000000000000000000000000000"
private_key = None
# UniSwap has the factory and router address by default
DEX_RATE = 0.003
uniswap_wrapper = Uniswap(address, private_key, version=2)
sushiswap_router = '0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F'
sushiswap_factory = '0xc2EdaD668740f1aA35E4D8f227fB8E17dcA888Cd'
sushiswap_wrapper = Uniswap(address, private_key, version=2,
                            factory_contract_addr=sushiswap_factory,
                            router_contract_addr=sushiswap_router)

# --- Monitoring prices ---
def print_titles():
  print('+-------------------++-------------------++-------------------------+')
  print('|     UniSwapV2     ||     SushiSwap     ||   Arbitrage Uni-Sushi   |')
  print('|-------------------||-------------------||-------------------------|')
  print('| SDT-IN  | SDT-OUT || SDT-IN  | SDT-OUT || Buy Ratio  | Sell Ratio |')
  print('|---------|---------||---------|---------||------------|------------|')

def print_prices():
  uni_sdt_in = uniswap_wrapper.get_eth_token_input_price(SDT_ADDR, eth_tokens)
  uni_sdt_out = uniswap_wrapper.get_token_eth_output_price(SDT_ADDR, eth_tokens)
  sushi_sdt_in  = sushiswap_wrapper.get_eth_token_input_price(SDT_ADDR, eth_tokens)
  sushi_sdt_out = sushiswap_wrapper.get_token_eth_output_price(SDT_ADDR, eth_tokens)

  uni_sdt_in, uni_sdt_out = uni_sdt_in / sdt_tokens, uni_sdt_out/ sdt_tokens
  sushi_sdt_in, sushi_sdt_out = sushi_sdt_in / sdt_tokens, sushi_sdt_out / sdt_tokens
 
  buy_ratio = (sushi_sdt_in * (1-DEX_RATE)) / (uni_sdt_out * (1+DEX_RATE))
  sell_ratio = (uni_sdt_in * (1-DEX_RATE)) / (sushi_sdt_out * (1+DEX_RATE))
  msg = '| {:.2f} | {:.2f} || {:.2f} | {:.2f} || {:.8f} | {:.8f} |'
  print(msg.format(uni_sdt_in, uni_sdt_out, sushi_sdt_in, sushi_sdt_out, buy_ratio, sell_ratio))
  Timer(5.0, print_prices).start()
  
print_titles()
print_prices()
