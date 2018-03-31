//PC寄存器和IF_ID寄存器之间有PC模块、InsMem、NPC模块
module regIF_ID(clk , rst , im_out , PC , IF_im_out , IF_PC,IF_IDWr);

    input       [31:0]      im_out;
    input       [31:0]      PC;
    input                   clk;
    input                   rst;
    input                   IF_IDWr;

    output  reg [31:0]      IF_im_out;
    output  reg [31:0]      IF_PC;

    always @(posedge clk or posedge rst)
    begin
        if( rst )
        begin
            IF_im_out <= 32'b0;
            IF_PC <= 32'b0;
        end
        else if(IF_IDWr)
        begin
            IF_im_out = im_out;
            IF_PC = PC;
        end
    end
endmodule