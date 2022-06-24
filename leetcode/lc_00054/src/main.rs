pub struct Solution {}

impl Solution {
    /// Given an m x n matrix, return all elements of the matrix in spiral order.
    pub fn spiral_order(matrix: Vec<Vec<i32>>) -> Vec<i32> {
        let mut result = Vec::new();
        if matrix.is_empty() {
            return result;
        }
        if matrix.len() == 1 {
            return matrix[0].clone();
        }

        if matrix[0].len() == 1 {
            for i in 0..matrix.len() {
                result.push(matrix[i][0]);
            }
            return result;
        }
        
        let mut row_start = 0;
        let mut row_end = matrix.len() - 1;
        let mut col_start = 0;
        let mut col_end = matrix[0].len() - 1;
        while row_start <= row_end && col_start <= col_end {
            for i in col_start..=col_end {
                result.push(matrix[row_start][i]);
            }
            row_start += 1;
            for i in row_start..=row_end {
                result.push(matrix[i][col_end]);
            }
            col_end -= 1;
            if row_start <= row_end {
                for i in (col_start..=col_end).rev() {
                    result.push(matrix[row_end][i]);
                }
            }
            row_end -= 1;
            if col_start <= col_end {
                for i in (row_start..=row_end).rev() {
                    result.push(matrix[i][col_start]);
                }
            }
            col_start += 1;
        }
        result
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    pub fn simple() {
        assert_eq!(
            Solution::spiral_order(vec![
                vec![1, 2, 3],
                vec![4, 5, 6],
                vec![7, 8, 9],
            ]),
            vec![1, 2, 3, 6, 9, 8, 7, 4, 5]
        );
    }

    #[test]
    pub fn simple_2() {
        assert_eq!(
            Solution::spiral_order(vec![
                vec![1, 2, 3, 4],
                vec![5, 6, 7, 8],
                vec![9, 10, 11, 12],
                vec![13, 14, 15, 16],
            ]),
            vec![1, 2, 3, 4, 8, 12, 16, 15, 14, 13, 9, 5, 6, 7, 11, 10]
        );
    }

    #[test]
    pub fn one_item() {
        assert_eq!(
            Solution::spiral_order(vec![
                vec![1],
            ]),
            vec![1]
        );
    }
    
    #[test]
    pub fn one_col() {
        assert_eq!(
            Solution::spiral_order(vec![
                vec![1],
                vec![2],
                vec![3]
            ]),
            vec![1,2,3]
        );
    }
    
    #[test]
    pub fn one_row() {
        assert_eq!(
            Solution::spiral_order(vec![
                vec![1,2,3]
            ]),
            vec![1,2,3]
        );
    }
    
}

fn main() {}
