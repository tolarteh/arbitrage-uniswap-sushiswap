from dotenv import dotenv_values
from web3 import Web3

config = dotenv_values(".env")

w3 = Web3(Web3.HTTPProvider(config["PROVIDER"]))
print("Connection =", w3.isConnected())
# token, amount_token, min_token, min_eth, to, deadline


def send_transaction(func, params):
  tx = func.buildTransaction(params)
  signed_tx = self.conn.eth.account.sign_transaction(tx, private_key=self.private_key)
  return self.conn.eth.sendRawTransaction(signed_tx.rawTransaction)



def add_liquidity_eth(token, amount_token, amount_eth, min_token, min_eth, to, deadline):
  """
  Add liquidity to an ERC20-WETH pool with ETH.
  :param token: Address of a pool token.
  :param amount_token: Amount of token to add as liquidity.
  :param amount_eth: Amount of ETH to add as liquidity.
  :param min_token: Bound to the extent to which the WETH/token price can go up before the transaction reverts
  :param min_eth: Bound to the extent to which the token/WETH price can go up before the transaction reverts.
  :param to: Address of the recipient for the liquidity tokens.
  :param deadline: Unix timestamp after which the transaction will revert.
  :return:
      - amount_token - Amount of token sent to the pool.
      - amount_eth - Amount of ETH converted to WETH and sent to the pool.
      - liquidity - Amount of liquidity tokens minted.
  """
  self.approve(token, amount_token)
  func = self.router.functions.addLiquidityETH(token, amount_token, min_token, min_eth, to, deadline)
  params = self._create_transaction_params(amount_eth)  # FIXME
  return self._send_transaction(func, params)