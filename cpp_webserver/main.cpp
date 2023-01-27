#include "multi_client.h"



int main() {
    multic::MultiClient mc("0.0.0.0", 27015);
    if (mc.init() != 0) {
        return 1;
    }

    mc.start();

    system("pause");
    return 0;
}