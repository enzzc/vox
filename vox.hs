import Data.Maybe
import Data.Either
import Data.List (foldl')

data Value = Start
          | R Float
          | I Int
          | Vi [Int]
          | Vf [Float]
          | S String
          | BinOp (Value -> Value -> Value)
          | Op (Value -> Value)

instance Show Value where
    show (I n)  = "I " ++ show n
    show (R x)  = "R " ++ show x
    show (Vi v) = "V " ++ show v
    show (Vf v) = "V " ++ show v

op_table = [
     ("sum", sum_)
    ]

binop_table = [
     ("+", add_)
    ]

add_ :: Value -> Value -> Value
add_ (I n) (I m) = I $ n + m
add_ (Vi v) (Vi u) = Vi $ zipWith (+) u v
add_ (Vf v) (Vf u) = Vf $ zipWith (+) u v

sum_ :: Value -> Value
sum_ (Vi v) = I $ sum v
sum_ (Vf v) = R $ sum v

eval_units :: Value -> Value -> Value
eval_units Start u2 = u2
eval_units u1 (BinOp binop) = Op $ binop u1
eval_units u1 (Op op) = op u1
eval_units (Op op) u2 = op u2
eval_units _ _ = error "Type"

eval_ast = foldl' eval_units Start
