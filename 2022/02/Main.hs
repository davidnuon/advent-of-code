import System.IO
import qualified Data.Text as T

data Shape = Rock | Paper | Scissors deriving (Show, Eq)
data MatchResult = Win | Lose | Draw deriving (Show, Eq)

both :: (a -> b) -> (a, a) -> (b, b)
both f (a, b) = (f a, f b)

instance Enum Shape where
    fromEnum Rock = 1
    fromEnum Paper = 2
    fromEnum Scissors = 3

    toEnum 1 = Rock
    toEnum 2 = Paper
    toEnum 3 = Scissors

instance Enum MatchResult where
    fromEnum Win = 6
    fromEnum Draw = 3
    fromEnum Lose = 0

    toEnum 6 = Win
    toEnum 3 = Draw
    toEnum 0 = Lose

shape2win :: Shape -> Shape
shape2win Rock = Paper
shape2win Paper = Scissors
shape2win Scissors = Rock

shape2lose :: Shape -> Shape
shape2lose Rock = Scissors
shape2lose Paper = Rock
shape2lose Scissors = Paper

getNeededShape :: MatchResult -> Shape -> Shape
getNeededShape Win = shape2win
getNeededShape Draw = id
getNeededShape Lose = shape2lose

computeMatchup :: Shape -> Shape -> MatchResult
computeMatchup them us
    | them == us = Draw
    | them == shape2win us = Lose
    | them == shape2lose us = Win

rps2Shape :: Char -> Shape
rps2Shape 'A' = Rock
rps2Shape 'B' = Paper
rps2Shape 'C' = Scissors
rps2Shape 'X' = Rock
rps2Shape 'Y' = Paper
rps2Shape 'Z' = Scissors
rps2Shape _ = error "Invalid shape code."

code2result :: Char -> MatchResult
code2result 'X' = Lose
code2result 'Y' = Draw
code2result 'Z' = Win

token2pair :: String -> (Char, Char)
token2pair token = (head token, last token)

part1calc lines = 
    let
        tokens = map token2pair lines
        us = map (fromEnum . rps2Shape . snd) tokens
        resultCalc = fromEnum . (uncurry computeMatchup) . (both rps2Shape)
        results = map resultCalc tokens
        scores = map (uncurry (+)) $ zip us results
    in 
        sum scores

part2calc lines = 
    let
        tokens = map token2pair lines
        neededResults = map (code2result . snd) tokens
        opponentShapes = map (rps2Shape . fst) tokens
        neededShapes = map (uncurry getNeededShape) $ zip neededResults opponentShapes
    in 
        sum $ map (uncurry (+)) $ zip (map fromEnum neededResults) (map fromEnum neededShapes)
main = 
    do
        lines <- getInput
        putStrLn $ (++) "Part 1: " $ show (part1calc lines)
        putStrLn $ (++) "Part 2: " $ show (part2calc lines)        

getInput = do
    lines <- getContents
    return $ map T.unpack $ T.splitOn (T.pack "\n") (T.pack lines)