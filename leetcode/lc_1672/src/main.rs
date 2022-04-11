pub struct Solution {}

fn main() {
    let sol = Solution::maximum_wealth;
    assert_eq!(sol(vec![vec![1,2,3],vec![3,2,1]]),6);
    assert_eq!(sol(vec![vec![1,5],vec![7,3],vec![3,5]]),10);
    assert_eq!(sol(vec![vec![2,8,7],vec![7,1,3],vec![1,9,5]]),17);
    
}

///You are given an m x n integer grid accounts where accounts[i][j] is the amount of money the i​​​​​​​​​​​th​​​​ customer has in the j​​​​​​​​​​​th​​​​ bank. Return the wealth that the richest customer has.
/// A customer's wealth is the amount of money they have in all their bank accounts. The richest customer is the customer that has the maximum wealth.
impl Solution {
    pub fn maximum_wealth(accounts: Vec<Vec<i32>>) -> i32 {
        let mut largest = 0;
        for cust in accounts {
            let wealth = cust.into_iter().reduce(|accum, item| { accum + item });
            if wealth.unwrap() > largest { largest = wealth.unwrap(); }

        }
        largest
    }
}
