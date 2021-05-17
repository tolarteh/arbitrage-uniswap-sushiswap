from uniswap import Uniswap
import os

infura_url = "https://mainnet.infura.io/v3/163e368fa52d4fe39ed32f3f8635f6ce"
os.environ["PROVIDER"] = infura_url

# library works by default with uniswap v2, so we need to pass
#  sushiswap router and factory
sushiswap_router = '0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F'
sushiswap_factory = '0xc2EdaD668740f1aA35E4D8f227fB8E17dcA888Cd'

address = "0x0000000000000000000000000000000000000000"  # change if you are making transactions
private_key = None  # change if making transactions.

uniswap_wrapper = Uniswap(address, private_key,
                          version=2)  # pass version=2 to use Uniswap v2

# useful token address
eth = "0x0000000000000000000000000000000000000000"
bat = "0x0D8775F648430679A709E98d2b0Cb6250d2887EF"
dai = "0x89d24A6b4CcB1B6fAA2625fE562bDD9a23260359"
sdt = "0x73968b9a57c6E53d41345FD57a6E6ae27d6CDB2F"

# I have exactly 1 eth, how many tokens can I get?
print(uniswap_wrapper.get_eth_token_input_price(sdt, 1))

# I have exactly 1 token, how many eth can I get?
print(uniswap_wrapper.get_token_eth_input_price(sdt, 1 * 10**12))

# I want exactly 1 token, how many eth do I need?
print(uniswap_wrapper.get_eth_token_output_price(sdt, 1 * 10**12))

# I want exactly 1 eth, how many tokens do I need.
print(uniswap_wrapper.get_token_eth_output_price(sdt, 1))

# ----------------SUSHISWAP-------------------------------------

sushiswap_wrapper = Uniswap(address,
                            private_key,
                            version=2,
                            factory_contract_addr=sushiswap_factory,
                            router_contract_addr=sushiswap_router)

# I have exactly 1 eth, how many tokens can I get?
print(sushiswap_wrapper.get_eth_token_input_price(sdt, 1))

print(sushiswap_wrapper.get_token_eth_input_price(sdt, 1 * 10**12))
print(sushiswap_wrapper.get_eth_token_output_price(sdt, 1 * 10**12))

# token to eth output price. I want exactly 1 eth, how many tokens do I need.
print(sushiswap_wrapper.get_token_eth_output_price(sdt, 1))