export declare const contract =
  '{ parameter (pair (set (pair (pair string bytes) string)) bool) ;\n  storage\n    (pair (pair (set %claims (pair (pair string bytes) string)) (string %contract_type))\n          (pair (big_map %metadata string bytes) (address %owner))) ;\n  code { UNPAIR ;\n         SWAP ;\n         DUP ;\n         DUG 2 ;\n         CDR ;\n         CDR ;\n         SENDER ;\n         COMPARE ;\n         NEQ ;\n         IF { PUSH string "Unauthorized." ; FAILWITH } {} ;\n         UNPAIR ;\n         DUP 3 ;\n         CDR ;\n         CDR ;\n         DUP 4 ;\n         CDR ;\n         CAR ;\n         PAIR ;\n         DUP 4 ;\n         CAR ;\n         CDR ;\n         DIG 4 ;\n         CAR ;\n         CAR ;\n         DIG 3 ;\n         ITER { SWAP ; DUP 5 ; DIG 2 ; UPDATE } ;\n         DIG 3 ;\n         DROP ;\n         PAIR ;\n         PAIR ;\n         NIL operation ;\n         PAIR } }';
