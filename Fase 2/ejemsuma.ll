
source_filename = "ejemsuma.dsl"

; --- Funciones externas del núcleo de Arduino ---
declare void @pinMode(i32, i32)
declare void @digitalWrite(i32, i32)
declare i32 @digitalRead(i32)
declare void @delay(i32)

define i32 @main() {
entry:
  %a.addr = alloca i32, align 4
  %b.addr = alloca i32, align 4
  %suma.addr = alloca i32, align 4
  %resta.addr = alloca i32, align 4
  %mult.addr = alloca i32, align 4
  %div.addr = alloca i32, align 4
  %resto.addr = alloca i32, align 4
  %i.addr = alloca i32, align 4
  %total.addr = alloca i32, align 4
  store i32 0, ptr %a.addr, align 4
  store i32 0, ptr %b.addr, align 4
  store i32 0, ptr %suma.addr, align 4
  store i32 0, ptr %resta.addr, align 4
  store i32 0, ptr %mult.addr, align 4
  store i32 0, ptr %div.addr, align 4
  store i32 0, ptr %resto.addr, align 4
  store i32 0, ptr %i.addr, align 4
  store i32 0, ptr %total.addr, align 4
  store i32 7, ptr %a.addr, align 4
  store i32 5, ptr %b.addr, align 4
  %a.val1 = load i32, ptr %a.addr, align 4
  %b.val2 = load i32, ptr %b.addr, align 4
  %t1 = add i32 %a.val1, %b.val2
  store i32 %t1, ptr %suma.addr, align 4
  %a.val3 = load i32, ptr %a.addr, align 4
  %b.val4 = load i32, ptr %b.addr, align 4
  %t2 = sub i32 %a.val3, %b.val4
  store i32 %t2, ptr %resta.addr, align 4
  ; --- línea 7 del programa DSL ---
  %a.val5 = load i32, ptr %a.addr, align 4
  %b.val6 = load i32, ptr %b.addr, align 4
  %t3 = mul i32 %a.val5, %b.val6
  store i32 %t3, ptr %mult.addr, align 4
  ; --- línea 8 del programa DSL ---
  %a.val7 = load i32, ptr %a.addr, align 4
  %b.val8 = load i32, ptr %b.addr, align 4
  %t4 = sdiv i32 %a.val7, %b.val8
  store i32 %t4, ptr %div.addr, align 4
  ; --- línea 9 del programa DSL ---
  %a.val9 = load i32, ptr %a.addr, align 4
  %b.val10 = load i32, ptr %b.addr, align 4
  %t5 = srem i32 %a.val9, %b.val10
  store i32 %t5, ptr %resto.addr, align 4
  ; --- línea 11 del programa DSL ---
  %suma.val11 = load i32, ptr %suma.addr, align 4
  call void @delay(i32 %suma.val11)
  ; --- línea 12 del programa DSL ---
  %resta.val12 = load i32, ptr %resta.addr, align 4
  call void @delay(i32 %resta.val12)
  ; --- línea 13 del programa DSL ---
  %mult.val13 = load i32, ptr %mult.addr, align 4
  call void @delay(i32 %mult.val13)
  ; --- línea 14 del programa DSL ---
  %div.val14 = load i32, ptr %div.addr, align 4
  call void @delay(i32 %div.val14)
  ; --- línea 15 del programa DSL ---
  %resto.val15 = load i32, ptr %resto.addr, align 4
  call void @delay(i32 %resto.val15)
  ; --- línea 17 del programa DSL ---
  store i32 1, ptr %i.addr, align 4
  ; --- línea 18 del programa DSL ---
  store i32 0, ptr %total.addr, align 4
  ; --- línea 19 del programa DSL ---
  br label %while_cond_1

while_cond_1:
  %i.val16 = load i32, ptr %i.addr, align 4
  %t6 = icmp sle i32 %i.val16, 5
  br i1 %t6, label %while_body_1, label %while_end_1

while_body_1:
  ; --- línea 20 del programa DSL ---
  %total.val17 = load i32, ptr %total.addr, align 4
  %i.val18 = load i32, ptr %i.addr, align 4
  %t7 = add i32 %total.val17, %i.val18
  store i32 %t7, ptr %total.addr, align 4
  ; --- línea 21 del programa DSL ---
  %i.val19 = load i32, ptr %i.addr, align 4
  %t8 = add i32 %i.val19, 1
  store i32 %t8, ptr %i.addr, align 4
  ; --- línea 19 del programa DSL ---
  br label %while_cond_1

while_end_1:
  ; --- línea 23 del programa DSL ---
  %total.val20 = load i32, ptr %total.addr, align 4
  call void @delay(i32 %total.val20)
  ret i32 0
}
