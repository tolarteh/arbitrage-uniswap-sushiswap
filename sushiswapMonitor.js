const { ethers } = require("ethers");

// instructions to install this npm init

const provider = new ethers.providers.JsonRpcProvider("https://mainnet.infura.io/v3/163e368fa52d4fe39ed32f3f8635f6ce");

//console.log('provider', provider)

// https://info.uniswap.org/pair/0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc

// uniswap pair address 0xc465c0a16228ef6fe1bf29c04fdb04bb797fd537
const uniswapSDTETHExchange = "0xc465c0a16228ef6fe1bf29c04fdb04bb797fd537";
 
// sushiswap pair address
const uniswapUsdtWethExchange = "0x22def8cf4e481417cb014d9dc64975ba12e3a184";

// this ABI object works for both Uniswap and SushiSwap
const uniswapAbi = [
  "event Swap(address indexed sender, uint amount0In, uint amount1In, uint amount0Out, uint amount1Out, address indexed to)",
];

function getAmountsFromSwapArgs(swapArgs) {
  const { amount0In, amount0Out, amount1In, amount1Out } = swapArgs;
  // 1. The eq method is for objects created
  //    from ethers.js BigNumber helper
  // 2. Note, this code only handles simple one-to-one token swaps.
  //    (It's also possible to swap both token0 and token1 for token0 and token1)
  let token0AmountBigDecimal = amount0In;
  if (token0AmountBigDecimal.eq(0)) {
    token0AmountBigDecimal = amount0Out;
  }

  let token1AmountBigDecimal = amount1In;
  if (token1AmountBigDecimal.eq(0)) {
    token1AmountBigDecimal = amount1Out;
  }

  return { token0AmountBigDecimal, token1AmountBigDecimal };
}

function convertSwapEventToPrice({ swapArgs, token0Decimals, token1Decimals }) {
  const {
    token0AmountBigDecimal,
    token1AmountBigDecimal,
  } = getAmountsFromSwapArgs(swapArgs);

  const token0AmountFloat = parseFloat(
    ethers.utils.formatUnits(token0AmountBigDecimal, token0Decimals)
  );
  const token1AmounFloat = parseFloat(
    ethers.utils.formatUnits(token1AmountBigDecimal, token1Decimals)
  );

  if (token1AmounFloat > 0) {
    const priceOfToken0InTermsOfToken1 = token0AmountFloat / token1AmounFloat;
    return { price: priceOfToken0InTermsOfToken1, volume: token0AmountFloat };
  }

  return null;
}

const uniswapContract = new ethers.Contract(
  uniswapUsdtWethExchange,
  uniswapAbi,
  provider
);
const filter = uniswapContract.filters.Swap();

uniswapContract.on(filter, (from, a0in, a0out, a1in, a1out, to, event) => {
  const { price, volume } = convertSwapEventToPrice({
    swapArgs: event.args,
    // the USDC ERC20 uses 6 decimals
    token0Decimals: 6,
    // the WETH ERC20 uses 18 decimals
    token1Decimals: 18,
  });
  console.log({ price, volume });
});