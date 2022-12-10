import System.IO
import qualified Data.Text as T
import Data.List (sort, reverse)

collectBags :: [String] -> [Int]
collectBags =
    let 
        collectBag currentBags "" = currentBags ++ [0]
        collectBag currentBags item = 
            let
                amount = read item :: Int
            in
                (init currentBags) ++ [(+) (last currentBags) amount]
    in
        foldl collectBag [0]

part2Function = sum . (take 3) . reverse . sort 

main = 
    do
        lines <- getInput
        bags <- pure $ collectBags lines
        putStrLn $ "Part 1: " ++ show (maximum bags)
        putStrLn $ "Part 2: " ++ show (part2Function bags)

getInput = do
    lines <- getContents   
    return $ map T.unpack $ T.splitOn (T.pack "\n") (T.pack lines)
