// Advent of Code 2024
// Dr Lee A. Christie
//
// GitHub:   @leechristie
// Mastodon: @0x1ac@techhub.social
// Website:  leechristie.com

import java.io.IOException;

public class Main {

    public static void main(String[] args) throws IOException {

        if (args.length < 1) {
            System.err.println("missing argument");
            System.exit(1);
        }

        if (args.length > 1) {
            System.err.println("too many arguments");
            System.exit(1);
        }

        if (args[0].equals("9")) {
            Day09.solve();
            return;
        }

        System.err.println("too many arguments");
        System.exit(1);

    }

}
