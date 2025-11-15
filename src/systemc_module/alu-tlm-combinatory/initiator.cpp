#include "initiator.h"
#include <iostream>

Initiator::Initiator(sc_core::sc_module_name name)
    : sc_module(name), initiator_socket("initiator_socket") {
}

alu_data_t Initiator::send_data(const alu_data_t &data) {
    // cout << "[INITIATOR]  Setting and sending data to initiator" << endl;
    alu_data_t alu_data = data;
    tlm::tlm_generic_payload trans;
    sc_time delay = sc_time(0, SC_NS);

    trans.set_command(tlm::TLM_WRITE_COMMAND);
    trans.set_data_ptr(reinterpret_cast<unsigned char *>(&alu_data));
    trans.set_data_length(sizeof(alu_data_t));
    trans.set_streaming_width(sizeof(alu_data_t));
    trans.set_response_status(tlm::TLM_INCOMPLETE_RESPONSE);

    initiator_socket->b_transport(trans, delay);

    if (trans.is_response_error()) {
        SC_REPORT_ERROR("TLM-2", "Transaction failed");
        return data; // Return original data on error
    } else {
        // Get the updated data from the transaction
        alu_data_t *received_data = reinterpret_cast<alu_data_t *>(trans.get_data_ptr());
        
        // std::cout << "[INITIATOR]  Transaction completed with result: " << received_data->result << std::endl;
        
        // Return the updated data
        return *received_data;
    }
}