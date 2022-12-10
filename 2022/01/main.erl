-module(main).
-export([main/1]).
-import(lists,[reverse/1]). 

main(_) -> 
    Lines = read_stdin([]),
    Bags = list_to_bags(Lines, [0]),
    BiggestBag = lists:max(Bags),
    SumTop3 = lists:sum(lists:sublist(reverse(lists:sort(Bags)), 3)),
    io:fwrite(io:format("Part 1: ~p\nPart 2: ~p\n", [BiggestBag, SumTop3])).

list_to_bags([], Bags) ->
    Bags;

list_to_bags([Head|Tail], Bags) ->
    TrimmedHead = string:trim(Head),
    case TrimmedHead of
        "" ->
            list_to_bags(Tail, Bags ++ [0]);
        _ ->
            [BagTail|BagInitReversed] = reverse(Bags),
            {PartNumber, _} = string:to_integer(TrimmedHead),
            NewBagTail = BagTail + PartNumber,
            list_to_bags(Tail, reverse([NewBagTail|BagInitReversed]))
    end.

read_stdin(Acc) ->
    case io:get_line("") of
        eof ->
            Acc; 
        Line ->
            read_stdin(Acc ++ [Line])
    end.