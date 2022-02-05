---
title: MIPS汇编语言（一）
date: 2021-11-16 23:49:14
tags: MIPS
categories: Assembly Language
---

### MIPS汇编语言入门

MIPS(Millions of Instructions Per Second)

**Classic flow**:

+ Fetch instruction
+ Read registers
+ Arithmetic operation
+ Memory access
+ Write back

Five steps and four cycles(Read and write registers cost only half a cycle).

Delay slot:

After the jump and branch condition, there is a delay slot to fill a non-related operation(usually a n operation before the branch).

### How a program excutes

+ genera 3-operand format

  ```assembly
  op	dest, src1, src2
  ```

### MIPS instructions & memory organization

+ type of instructions

  ![image-20211117001847724](C:\Users\19749\AppData\Roaming\Typora\typora-user-images\image-20211117001847724.png)

  - Data operations
    - Arithmetic(add, substrct……)
    - Logical(and, or, not, xor……)
  - Data transfer
    - Load(Memory -> Register)
    - Store(Register -> Memory)
  - Sequencing
    - Branch(conditional, >, <, ==……)
    - Jump(unconditional, goto……)

+ Registers

  - 32 General Purpose Registers
  - **Very important!! **
    - **ALL the values for instructions must come from registers!**
    - **R0 is always zero!!**

### Data operations & transfers

### Sequencing



