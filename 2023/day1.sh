#!/usr/bin/env bash

# Strip out all alphas, fixup single digits, strip out middle digits
part_1=$(cat day1.txt | sed -r -e 's:[a-zA-Z]::g ; s:^([0-9])$:\1\1:g ; s:^(.)[0-9]+(.)$:\1\2:g' | paste -sd+ | bc)

# Insert digits and repeat script above
part_2=$(cat day1.txt | sed -r -e ' s:one:&1&:g;
                                    s:two:&2&:g;
                                    s:three:&3&:g;
                                    s:four:&4&:g;
                                    s:five:&5&:g;
                                    s:six:&6&:g;
                                    s:seven:&7&:g;
                                    s:eight:&8&:g;
                                    s:nine:&9&:g;
                                    s:[a-zA-Z]::g; s:^([0-9])$:\1\1:g ; s:^(.)[0-9]+(.)$:\1\2:g' | paste -sd+ | bc)


echo Part 1: ${part_1}
echo Part 2: ${part_2}
