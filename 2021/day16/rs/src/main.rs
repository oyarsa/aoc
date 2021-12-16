#![allow(dead_code, unused_variables)]

use std::io::stdin;

fn hex_to_bin(hex: &str) -> String {
    hex.chars().map(hex_digit).collect()
}

fn hex_digit(d: char) -> &'static str {
    match d {
        '0' => "0000",
        '1' => "0001",
        '2' => "0010",
        '3' => "0011",
        '4' => "0100",
        '5' => "0101",
        '6' => "0110",
        '7' => "0111",
        '8' => "1000",
        '9' => "1001",
        'A' => "1010",
        'B' => "1011",
        'C' => "1100",
        'D' => "1101",
        'E' => "1110",
        'F' => "1111",
        _ => unreachable!(),
    }
}

fn main() {
    let mut buf = String::new();
    let stdin = stdin().read_line(&mut buf).unwrap();
    println!("Part 1: {}", part1(&buf.trim()));
    println!("Part 2: {}", part2(&buf.trim()));
}

fn part1(input: &str) -> usize {
    let pkt = parse(input);
    sum(&pkt)
}

fn part2(input: &str) -> usize {
    let pkt = parse(input);
    interpret(&pkt)
}

fn sum(pkt: &Packet) -> usize {
    pkt.version
        + match &pkt.payload {
            Payload::SubPackets(packets) => packets.iter().map(sum).sum(),
            Payload::Literal(x) => 0,
        }
}

fn interpret(pkt: &Packet) -> usize {
    match pkt.typeid {
        4 => pkt.payload.value(),
        0 => pkt.payload.iter().map(interpret).sum(),
        1 => pkt.payload.iter().map(interpret).product(),
        2 => pkt.payload.iter().map(interpret).min().unwrap(),
        3 => pkt.payload.iter().map(interpret).max().unwrap(),
        5 => {
            let mut p = pkt.payload.iter().take(2);
            let (a, b) = (p.next().unwrap(), p.next().unwrap());
            if interpret(a) > interpret(b) {
                1
            } else {
                0
            }
        }
        6 => {
            let mut p = pkt.payload.iter().take(2);
            let (a, b) = (p.next().unwrap(), p.next().unwrap());
            if interpret(a) < interpret(b) {
                1
            } else {
                0
            }
        }
        7 => {
            let mut p = pkt.payload.iter().take(2);
            let (a, b) = (p.next().unwrap(), p.next().unwrap());
            if interpret(a) == interpret(b) {
                1
            } else {
                0
            }
        }
        _ => unreachable!(),
    }
}

#[derive(Debug, PartialEq)]
struct Packet {
    version: usize,
    typeid: usize,
    payload: Payload,
}

#[derive(Debug, PartialEq)]
enum Payload {
    SubPackets(Vec<Packet>),
    Literal(usize),
}

impl Payload {
    fn value(&self) -> usize {
        match self {
            Payload::Literal(x) => *x,
            _ => unreachable!(),
        }
    }

    fn iter(&self) -> impl Iterator<Item = &Packet> {
        match self {
            Payload::SubPackets(ps) => ps.iter(),
            _ => unreachable!(),
        }
    }
}

impl Packet {
    fn new_lit(version: usize, pkt_type: usize, lit: usize) -> Packet {
        Self {
            version,
            typeid: pkt_type,
            payload: Payload::Literal(lit),
        }
    }

    fn new_nested(version: usize, pkt_type: usize, packets: Vec<Packet>) -> Packet {
        Self {
            version,
            typeid: pkt_type,
            payload: Payload::SubPackets(packets),
        }
    }
}

fn parse(hex: &str) -> Packet {
    let i = hex_to_bin(hex);
    let (pkt, _) = parse_packet(&i);
    pkt
}

fn parse_packet(i: &'_ str) -> ParseResult<'_, Packet> {
    let (version, i) = be_n(&i, 3);
    let (typeid, i) = be_n(&i, 3);

    match typeid {
        4 => {
            let (lit, i) = parse_literal(i);
            (Packet::new_lit(version, typeid, lit), i)
        }
        _ => {
            let (pkts, i) = parse_operator(i);
            (Packet::new_nested(version, typeid, pkts), i)
        }
    }
}

fn parse_operator(i: &'_ str) -> ParseResult<'_, Vec<Packet>> {
    let (length_id, i) = be_n(i, 1);
    match length_id {
        0 => {
            let (len, i) = be_n(i, 15);
            let (pkt, i) = str_n(i, len);
            let (pkts, _) = parse_type0(pkt);
            (pkts, i)
        }
        1 => {
            let (n, i) = be_n(i, 11);
            parse_type1(i, n)
        }
        _ => unreachable!(),
    }
}

type ParseResult<'a, T> = (T, &'a str);

fn bin_to_int(s: &str) -> usize {
    usize::from_str_radix(s, 2).unwrap_or_else(|_| panic!("Invalid binary string: {}", s))
}

fn be_n(i: &'_ str, n: usize) -> ParseResult<'_, usize> {
    let (version, rest) = str_n(i, n);
    let version = bin_to_int(version);
    (version, rest)
}

fn str_n(i: &'_ str, n: usize) -> ParseResult<'_, &'_ str> {
    i.split_at(n)
}

fn parse_literal(mut i: &'_ str) -> ParseResult<'_, usize> {
    let mut parts = vec![];
    let mut done = false;
    while !done {
        let (group_id, r) = be_n(i, 1);
        i = r;
        done = group_id == 0;
        let (lit, r) = str_n(i, 4);
        i = r;
        parts.push(lit);
    }
    let literal: String = parts.iter().cloned().collect();
    (bin_to_int(&literal), i)
}

fn parse_type0(mut i: &'_ str) -> ParseResult<'_, Vec<Packet>> {
    let mut pkts = vec![];
    while !i.is_empty() {
        let (pkt, r) = parse_packet(i);
        i = r;
        pkts.push(pkt);
    }
    (pkts, i)
}

fn parse_type1(mut i: &'_ str, n: usize) -> ParseResult<'_, Vec<Packet>> {
    let mut pkts = vec![];
    for _ in 0..n {
        let (pkt, r) = parse_packet(i);
        i = r;
        pkts.push(pkt);
    }
    (pkts, i)
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn literal_packet_steps() {
        let pkt = "D2FE28";
        let bin = hex_to_bin(pkt);
        assert_eq!(&bin, "110100101111111000101000");

        let (version, i) = be_n(&bin, 3);
        assert_eq!(version, 6);
        assert_eq!(i, "100101111111000101000");

        let (typeid, i) = be_n(&i, 3);
        assert_eq!(typeid, 4);
        assert_eq!(i, "101111111000101000");

        let mut literals = vec![];

        let (group_id, i) = be_n(&i, 1);
        assert_eq!(group_id, 1);
        assert_eq!(i, "01111111000101000");
        let (lit1, i) = str_n(&i, 4);
        assert_eq!(lit1, "0111");
        assert_eq!(i, "1111000101000");
        literals.push(lit1);

        let (group_id, i) = be_n(&i, 1);
        assert_eq!(group_id, 1);
        assert_eq!(i, "111000101000");
        let (lit2, i) = str_n(&i, 4);
        assert_eq!(lit2, "1110");
        assert_eq!(i, "00101000");
        literals.push(lit2);

        let (group_id, i) = be_n(&i, 1);
        assert_eq!(group_id, 0);
        assert_eq!(i, "0101000");
        let (lit3, i) = str_n(&i, 4);
        assert_eq!(lit3, "0101");
        assert_eq!(i, "000");
        literals.push(lit3);

        let literal: String = literals.iter().copied().collect();
        assert_eq!(literal, "011111100101");
        let literal = bin_to_int(&literal);
        assert_eq!(literal, 2021);
    }

    #[test]
    fn test_parse_literal() {
        let pkt = "D2FE28";
        let bin = hex_to_bin(pkt);
        let (version, i) = be_n(&bin, 3);
        let (typeid, i) = be_n(&i, 3);
        let (lit, _) = parse_literal(&i);
        let pkt = Packet::new_lit(version, typeid, lit);
        assert_eq!(pkt, Packet::new_lit(6, 4, 2021));
    }

    #[test]
    fn test_packet_literal() {
        let pkt = "D2FE28";
        let bin = hex_to_bin(pkt);
        let (pkt, i) = parse_packet(&bin);
        assert_eq!(pkt, Packet::new_lit(6, 4, 2021));
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2("C200B40A82"), 3);
        assert_eq!(part2("04005AC33890"), 54);
        assert_eq!(part2("880086C3E88112"), 7);
        assert_eq!(part2("CE00C43D881120"), 9);
        assert_eq!(part2("D8005AC2A8F0"), 1);
        assert_eq!(part2("F600BC2D8F"), 0);
        assert_eq!(part2("9C005AC2F8F0"), 0);
        assert_eq!(part2("9C0141080250320F1802104A08"), 1);
    }
}
