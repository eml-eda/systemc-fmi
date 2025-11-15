#include "top.h"
#include "Alu.h"
#include "initiator.h"

Top::Top(sc_core::sc_module_name name)
    : sc_module(name) {
    init = new Initiator("initiator");
    alu = new Alu("alu");

    init->initiator_socket.bind(alu->target_socket);
}

Top::~Top() {
    delete init;
    delete alu;
}

alu_data_t Top::send_data(const alu_data_t &data) {
    // std::cout << "Setting and sending data to initiator" << std::endl;

    // Get the result back from the initiator
    alu_data_t result = init->send_data(data);

    // std::cout << "Transaction completed" << std::endl;
    // std::cout << "result = " << result.result << std::endl;
    return result;
}