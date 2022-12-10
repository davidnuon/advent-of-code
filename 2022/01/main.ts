import { readLines } from "https://deno.land/std/io/buffer.ts";

async function getInput() {
    const lines = [];
    for await (const line of readLines(Deno.stdin)) {
        lines.push(line);
    }

    return lines;
}

async function main() {
    const input = await getInput();
    const bags = [0];    

    for (const line of input) {
        switch (line) {
            case "":
                bags.push(0);
                break;
            default:
                bags[bags.length - 1] += Number.parseInt(line);
                break;
        }
    }

    console.log('Part 1:', bags
                            .reduce((a, b) => Math.max(a, b), -1)
    );

    console.log('Part 2:', bags
                            .sort()
                            .slice(0, 3)
                            .reduce((a, b) => a + b, 0)
    );
}

await main();
