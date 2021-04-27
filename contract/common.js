const contract = `{ parameter
    (or (set %addClaims (pair (pair string bytes) string))
        (set %removeClaims (pair (pair string bytes) string))) ;
  storage
    (pair (pair (set %claims (pair (pair string bytes) string)) (string %contract_type))
          (pair (big_map %metadata string bytes) (address %owner))) ;
  code { UNPAIR ;
         SWAP ;
         DUP ;
         DUG 2 ;
         CDR ;
         CDR ;
         SENDER ;
         COMPARE ;
         NEQ ;
         IF { PUSH string "Unauthorized." ; FAILWITH } {} ;
         IF_LEFT
           { SWAP ;
             DUP ;
             DUG 2 ;
             CDR ;
             CDR ;
             DUP 3 ;
             CDR ;
             CAR ;
             PAIR ;
             DUP 3 ;
             CAR ;
             CDR ;
             DIG 3 ;
             CAR ;
             CAR ;
             DIG 3 ;
             ITER { PUSH bool True ; SWAP ; UPDATE } ;
             PAIR ;
             PAIR ;
             NIL operation ;
             PAIR }
           { SWAP ;
             DUP ;
             DUG 2 ;
             CDR ;
             CDR ;
             DUP 3 ;
             CDR ;
             CAR ;
             PAIR ;
             DUP 3 ;
             CAR ;
             CDR ;
             DIG 3 ;
             CAR ;
             CAR ;
             DIG 3 ;
             ITER { PUSH bool False ; SWAP ; UPDATE } ;
             PAIR ;
             PAIR ;
             NIL operation ;
             PAIR } } }`;

module.exports.contract = contract;
