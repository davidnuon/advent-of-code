#lang racket

(define (collect-bags lines bags)
  (cond
    [(null? lines) bags]
    [(string=? (car lines) "") (collect-bags (cdr lines) (cons 0 bags))]
    [else (collect-bags (cdr lines) (cons (+ (car bags) (string->number (car lines))) (cdr bags)))]))

(define (maximum xs)
  (define (max x1 x2)
    (if (> x1 x2) x1 x2))
  (foldl max -inf.0 xs))

(define (sum-of-first-three xs)
  (foldl + 0 (take (sort xs >) 3)))

(define (main)
  (define all-bags (collect-bags (slurp-stdin) '(0)))
  (define part1 (maximum all-bags))
  (define part2 (sum-of-first-three all-bags))
  (printf "Part 1: ~v\n" part1)
  (printf "Part 2: ~v\n" part2)
  )

(define (slurp-stdin)
  (let loop ([lines '()])
    (define line (read-line (current-input-port) 'any))
    (if (eof-object? line)
        (reverse lines)
        (loop (cons line lines)))))

(main)