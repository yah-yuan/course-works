module im_4k( addr, dout );
    
    input [9:0] addr;
    output [31:0] dout;
    
    reg [31:0] imem[1023:0];
    reg [31:0]  r_dout;
    
    always @(addr)
    begin
        r_dout = imem[addr];
    end
    assign dout = r_dout;
endmodule    
