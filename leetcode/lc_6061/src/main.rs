fn main() {
    assert_eq!(Solution::ways_to_buy_pens_pencils(20, 10, 5),9);
    assert_eq!(Solution::ways_to_buy_pens_pencils(5, 10, 10),1);
    assert_eq!(Solution::ways_to_buy_pens_pencils(100, 1, 1),5151);
    assert_eq!(Solution::ways_to_buy_pens_pencils(10, 99, 9),2);
    assert_eq!(Solution::ways_to_buy_pens_pencils(1000000, 1, 1),5000150001);

}

pub struct Solution {} 

impl Solution {
    pub fn ways_to_buy_pens_pencils(total: i32, cost1: i32, cost2: i32) -> i64 {
        let max_pens = 1 + (total/cost1);
        let mut count = 0;
        for pens in 0..max_pens {
            let max_pencils = (total - (pens*cost1))/cost2;
            count += max_pencils +1;
        }
        count as i64
    }
}
