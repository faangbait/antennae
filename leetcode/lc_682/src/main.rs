pub struct Solution {}
fn main() {
    let sol = Solution::cal_points;
    assert_eq!(sol(vec!["5".to_string(),"2".to_string(),"C".to_string(),"D".to_string(),"+".to_string()]), 30);
    assert_eq!(sol(vec!["5".to_string(),"-2".to_string(),"4".to_string(),"C".to_string(),"D".to_string(),"9".to_string(),"+".to_string(),"+".to_string()]),27);
    assert_eq!(sol(vec!["1".to_string()]),1);
   
}

impl Solution {

    /*
    You are keeping score for a baseball game with strange rules.
    The game consists of several rounds, where the scores of past rounds may affect future rounds' scores.

    At the beginning of the game, you start with an empty record.
    You are given a list of strings ops, where ops[i] is the ith operation you must apply to the record and is one of the following:

    1. An integer x - Record a new score of x.
    2. "+" - Record a new score that is the sum of the previous two scores. It is guaranteed there will always be two previous scores.
    3. "D" - Record a new score that is double the previous score. It is guaranteed there will always be a previous score.
    4. "C" - Invalidate the previous score, removing it from the record. It is guaranteed there will always be a previous score.

    Return the sum of all the scores on the record.
    */
    pub fn cal_points(ops: Vec<String>) -> i32 {
        let mut rounds: Vec<i32> =  vec![];
        let mut points: i32 = 0;

        for op in ops {
            let parsed_int = op.parse::<i32>();
            let parsed_char = op.parse::<char>();
            
            match parsed_int.ok() {
                Some(int) => rounds.push(int),
                None => match parsed_char.ok() {
                    Some(char) => match char {
                        'C' => rounds.truncate(rounds.len()-1),
                        'D' => rounds.push(rounds.last().unwrap()*2),
                        '+' => {
                            rounds.push(rounds[rounds.len()-1] + rounds[rounds.len()-2]);
                        },
                        _ => panic!(),
                    },
                    None => panic!()
                }
            };

        }
        for round in rounds {
            points += round;
        }
        return points;
    }
}
