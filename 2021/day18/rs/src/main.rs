use std::{
    io::{stdin, BufRead},
    ops::Add,
};

use itertools::Itertools;
use regex::Regex;

#[derive(Debug, Clone, Copy, PartialEq)]
struct Element {
    value: u32,
    depth: u32,
}

impl Element {
    fn new(value: u32, depth: u32) -> Self {
        Self { value, depth }
    }
}

#[derive(Clone, Debug, Default, PartialEq)]
struct Number(Vec<Element>);

impl Add for &Number {
    type Output = Number;

    fn add(self, rhs: Self) -> Self::Output {
        let mut a = self.clone();
        a.0.append(&mut rhs.clone().0);
        a.0.iter_mut().for_each(|x| x.depth += 1);
        a.reduce()
    }
}

impl Number {
    fn magnitude(&self) -> u32 {
        let mut number = self.clone();
        for depth in (1..=4).rev() {
            while number.magreduce(depth) {}
        }
        number.0[0].value
    }
    fn magreduce(&mut self, depth: u32) -> bool {
        let nums = &mut self.0;
        for i in 0..nums.len() {
            if nums[i].depth == depth {
                let a = nums.remove(i);
                let b = nums.remove(i);
                nums.insert(i, Element::new(3 * a.value + 2 * b.value, depth - 1));
                return true;
            }
        }
        false
    }

    fn try_explode(&mut self) -> bool {
        let nums = &mut self.0;
        for i in 0..nums.len() {
            if nums[i].depth >= 5 {
                if i > 0 {
                    nums[i - 1].value += nums[i].value;
                }
                if i + 2 < nums.len() {
                    nums[i + 2].value += nums[i + 1].value;
                }
                nums[i].depth -= 1;
                nums[i].value = 0;
                nums.remove(i + 1);
                return true;
            }
        }
        false
    }

    fn try_split(&mut self) -> bool {
        let nums = &mut self.0;
        for i in 0..nums.len() {
            if nums[i].value >= 10 {
                let n = nums[i];
                let left = Element::new(n.value / 2, n.depth + 1);
                let right = Element::new(n.value / 2 + n.value % 2, n.depth + 1);
                nums.remove(i);
                nums.insert(i, left);
                nums.insert(i + 1, right);
                return true;
            }
        }
        false
    }

    fn reduce(mut self) -> Number {
        while self.try_explode() || self.try_split() {}
        self
    }
}

fn parse_line(line: &str) -> Number {
    let re = Regex::new(r"\[|\]|\d+").unwrap();
    let mut depth = 0;
    let mut numbers = vec![];
    for c in re.find_iter(line) {
        match c.as_str() {
            "[" => depth += 1,
            "]" => depth -= 1,
            c => {
                if let Ok(x) = c.parse::<u32>() {
                    numbers.push(Element::new(x, depth))
                }
            }
        }
    }
    Number(numbers)
}

fn read_problem() -> Vec<Number> {
    stdin()
        .lock()
        .lines()
        .flatten()
        .map(|x| parse_line(&x))
        .collect()
}

fn part1(problem: Vec<Number>) -> u32 {
    problem
        .into_iter()
        .reduce(|a, b| &a + &b)
        .unwrap()
        .magnitude()
}

fn part2(problem: Vec<Number>) -> u32 {
    problem
        .into_iter()
        .tuple_combinations()
        .flat_map(|(a, b)| [(&a + &b).magnitude(), (&b + &a).magnitude()])
        .max()
        .unwrap()
}

fn main() {
    let problem = read_problem();
    println!("Part 1: {}", part1(problem.clone()));
    println!("Part 2: {}", part2(problem));
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_explode() {
        let pairs = [
            ("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]"),
            ("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]"),
            ("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]"),
            (
                "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]",
                "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]",
            ),
            (
                "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]",
                "[[3,[2,[8,0]]],[9,[5,[7,0]]]]",
            ),
        ];

        for (inp, out) in pairs {
            let mut inp = parse_line(inp);
            let out = parse_line(out);
            inp.try_explode();
            assert_eq!(inp, out);
        }
    }

    #[test]
    fn test_split() {
        let pairs = [
            (
                "[[[[0,7],4],[15,[0,13]]],[1,1]]",
                "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]",
            ),
            (
                "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]",
                "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]",
            ),
        ];
        for (inp, out) in pairs {
            let mut inp = parse_line(inp);
            let out = parse_line(out);
            inp.try_split();
            assert_eq!(inp, out);
        }
    }

    #[test]
    fn test_split2() {
        let mut inp = Number(vec![
            Element {
                depth: 1,
                value: 10,
            },
            Element {
                depth: 1,
                value: 10,
            },
        ]);
        let mut out1 = Number(vec![
            Element { depth: 2, value: 5 },
            Element { depth: 2, value: 5 },
            Element {
                depth: 1,
                value: 10,
            },
        ]);
        let out2 = Number(vec![
            Element { depth: 2, value: 5 },
            Element { depth: 2, value: 5 },
            Element { depth: 2, value: 5 },
            Element { depth: 2, value: 5 },
        ]);

        inp.try_split();
        assert_eq!(inp, out1);
        out1.try_split();
        assert_eq!(out1, out2);
    }

    #[test]
    fn test_magnitude() {
        let pairs = [
            ("[[1,2],[[3,4],5]]", 143),
            ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384),
            ("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445),
            ("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791),
            ("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137),
            (
                "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",
                3488,
            ),
        ];
        for (num, mag) in pairs {
            let num = parse_line(num);
            assert_eq!(num.magnitude(), mag);
        }
    }
}
